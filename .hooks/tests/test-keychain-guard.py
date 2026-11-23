#!/usr/bin/env python3
"""Test the keychain_guard hooks shipped in the claude_code role defaults.

keychain_guard (PreToolUse) denies keychain reads and writes through the
`security` CLI, any reference to the keychain files, and launching `claude`
from a substitute HOME - the blank-home-plus-symlinked-keychain trick that
runs a signed-in session with none of the user's hooks. keychain_allow_prompt
(UserPromptSubmit) lifts the guard for one turn when the user's own prompt
says "allow keychain access", and keychain_allow_clear (Stop) ends it.

The guard has to stay narrow: Claude Code keeps its own login token in the
keychain, read-only listing is fine, and the user sometimes wants keychain
access on purpose. So the ALLOW matrix matters as much as BLOCK.

KNOWN_GAPS records what is deliberately not caught: each case has to be built
on purpose to slip past, and closing them means reimplementing a shell. They
are asserted to pass so the boundary stays explicit.

Each hook body is extracted from the shipped YAML and executed through `sh`
exactly as the hook harness runs it, under a throwaway HOME, so block-scalar
embedding and shell escaping are covered too.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
DEFAULTS = "roles/claude_code/defaults/main.yml"
GUARD, PROMPT, CLEAR = "keychain_guard", "keychain_allow_prompt", "keychain_allow_clear"

SQ = chr(39)
DQ = chr(34)
BT = chr(96)
DOLLAR = chr(36)
KC = "Library/Keychains"
FAKE_ITEM = "keychain-guard-test-nonexistent-item"

# (tool, tool_input, label) - every one of these must be denied by default.
BLOCK = [
    ("Bash", f"security find-generic-password -s {FAKE_ITEM}", "find-generic-password"),
    ("Bash", f"security find-generic-password -a me -s {FAKE_ITEM} -w", "password printed with -w"),
    ("Bash", "security find-internet-password -s github.com", "find-internet-password"),
    ("Bash", f"/usr/bin/security find-generic-password -s {FAKE_ITEM}", "absolute path"),
    ("Bash", f"security -v find-generic-password -s {FAKE_ITEM}", "global option first"),
    ("Bash", "sudo security dump-keychain", "dump-keychain under sudo"),
    ("Bash", "security export -t identities -f pkcs12 -o /tmp/out.p12", "export"),
    ("Bash", "security import /tmp/in.p12", "import"),
    ("Bash", "security unlock-keychain -p hunter2", "unlock-keychain"),
    ("Bash", "security add-generic-password -a a -s s -w w", "add-generic-password"),
    ("Bash", "security delete-generic-password -s s", "delete-generic-password"),
    ("Bash", "security set-key-partition-list -S apple: -k pw", "set-key-partition-list"),
    ("Bash", "security list-keychains -d user -s /tmp/evil", "list-keychains -s"),
    ("Bash", "security default-keychain -s other", "default-keychain -s"),
    ("Bash", "echo find-generic-password | security -i", "interactive mode"),
    ("Bash", f'bash -c "security find-generic-password -s {FAKE_ITEM}"', "bash -c"),
    ("Bash", 'eval "security dump-keychain"', "eval"),
    ("Bash", f"ls && security find-generic-password -s {FAKE_ITEM}", "second clause"),
    ("Bash", f"ln -s ~/{KC} /tmp/x", "symlink with tilde"),
    ("Bash", f"ln -s /Users/someone/{KC} /tmp/nm-evhome-r1/{KC}", "the original incident"),
    ("Bash", f'mkdir -p /tmp/h/Library && ln -s "{DOLLAR}HOME/{KC}" /tmp/h/{KC}', "symlink via HOME"),
    ("Bash", f"cp ~/{KC}/login.keychain-db /tmp/", "copy the keychain file"),
    ("Bash", f"rsync -a ~/{KC}/ /tmp/k/", "rsync"),
    ("Bash", "cat login.keychain-db", "keychain-db by name"),
    ("Bash", "cp old.keychain /tmp/", "legacy .keychain file"),
    ("Bash", f'ln -s ~/Library/"Keychains" /tmp/x', "quote spliced into the path"),
    ("Bash", "ls ~/library/keychains", "lower case path"),
    ("Bash", "env -i HOME=/tmp/nm-evhome-r1 claude plugin eval .", "env -i HOME= plugin eval"),
    ("Bash", "env -i HOME=/tmp/h PATH=/usr/bin /opt/bin/claude -p hi", "absolute claude path"),
    ("Bash", "HOME=/tmp/h claude -p hi", "HOME= prefix"),
    ("Bash", "export HOME=/tmp/h && claude -p hi", "export in an earlier clause"),
    ("Bash", "HOME=/tmp/h; claude", "bare assignment clause"),
    ("Bash", f"cd /tmp && HOME={DOLLAR}PWD/h claude -p x", "HOME from a variable"),
    ("Bash", 'HOME=/tmp/h bash -c "claude -p hi"', "override carried into a wrapper"),
    ("Bash", 'bash -c "HOME=/tmp/h claude -p hi"', "override inside a wrapper"),
    ("Read", {"file_path": f"/Users/someone/{KC}/login.keychain-db"}, "Read tool path"),
    ("Edit", {"file_path": "/tmp/h/login.keychain-db"}, "Edit tool path"),
    ("Glob", {"pattern": "**/*.keychain-db"}, "Glob pattern"),
]

# Denied even with the allowance: only the prompt hook may write the allowance.
ALWAYS_BLOCK = [
    ("Bash", "mkdir -p ~/.claude/keychain-allowance && touch ~/.claude/keychain-allowance/s1", "Bash allowance"),
    ("Write", {"file_path": "/home/x/.claude/keychain-allowance/s1", "content": "x"}, "Write allowance"),
]

# (tool, tool_input, label) - none of these may be denied.
ALLOW = [
    ("Bash", "ls -la", "unrelated command"),
    ("Bash", "echo hello world", "echo"),
    ("Bash", "security list-keychains", "list-keychains"),
    ("Bash", "security list-keychains -d user", "list-keychains for a domain"),
    ("Bash", "security default-keychain", "show the default keychain"),
    ("Bash", "security find-certificate -a -c Apple", "public certificates"),
    ("Bash", "security find-identity -v -p codesigning", "signing identities"),
    ("Bash", "security verify-cert -c cert.pem", "verify-cert"),
    ("Bash", "security", "bare security prints usage"),
    ("Bash", "which security && man security", "looking the tool up"),
    ("Bash", f"rg -n {SQ}find-generic-password{SQ} docs/", "searching for a subcommand"),
    ("Bash", f'grep -rn "security find-generic-password" .', "searching for a whole command"),
    ("Bash", "claude -p hi", "plain claude"),
    ("Bash", "claude plugin eval ./plugin", "plain plugin eval"),
    ("Bash", f"HOME={DOLLAR}HOME claude -p hi", "HOME kept as HOME"),
    ("Bash", "HOME=/tmp/h ansible-playbook site.yml", "HOME override for another tool"),
    ("Bash", "HOME=/tmp/h git status && claude -p hi", "override scoped to its own clause"),
    ("Bash", "git checkout -b fm/keychain-guard-hook", "branch name"),
    ("Bash", "git config credential.helper osxkeychain", "credential helper name"),
    ("Bash", "cat ~/.claude/settings.json", "reading settings"),
    ("Read", {"file_path": "/tmp/notes.md"}, "Read elsewhere"),
    ("Write", {"file_path": "/tmp/doc.md", "content": f"never symlink ~/{KC}"}, "Write prose naming the path"),
    ("Grep", {"pattern": KC, "path": "/repo"}, "Grep searching for the path"),
]

# Deliberately not caught: each has to be built on purpose to slip past.
KNOWN_GAPS = [
    ("Bash", f"security {DOLLAR}(echo find-generic-password) -s x", "command substitution"),
    ("Bash", f"echo {SQ}security dump-keychain{SQ} | sh", "script piped into sh"),
    ("Bash", "cd ~/Library && ln -s Keychains /tmp/x", "path split across a cd"),
    ("Bash", f"k=Keych; ln -s ~/Library/{DOLLAR}{{k}}ains /tmp/x", "path assembled from a variable"),
    ("Bash", f'python3 -c "import keyring; keyring.get_password({SQ}s{SQ}, {SQ}a{SQ})"', "another language"),
    ("Bash", f"bash -c {SQ}bash -c {DQ}security dump-keychain{DQ}{SQ}", "two levels of wrapping"),
]

# Positive control: a substring scanner must fail ALLOW, or ALLOW proves nothing.
LEGACY = (
    "python3 -c " + DQ + "import json, sys; d = json.load(sys.stdin); "
    "c = json.dumps(d.get('tool_input', {})).lower(); "
    "sys.exit(2 if 'keychain' in c or 'security' in c or 'home=' in c else 0)" + DQ
)


def block_at(lines, start):
    """Return the dedented body of the block scalar opened on line `start`."""
    base = len(lines[start]) - len(lines[start].lstrip())
    body = []
    for line in lines[start + 1:]:
        if not line.strip():
            body.append("")
            continue
        if len(line) - len(line.lstrip()) <= base:
            break
        body.append(line)
    cut = min(len(x) - len(x.lstrip()) for x in body if x.strip())
    return "\n".join(x[cut:] for x in body).rstrip("\n")


def extract(key):
    """Pull the `command: |` block scalar of the hook named `key`."""
    lines = (REPO / DEFAULTS).read_text().split("\n")
    starts = [i for i, line in enumerate(lines) if line == f"  {key}:"]
    if len(starts) != 1:
        raise SystemExit(f"{DEFAULTS}: expected 1 {key} hook, found {len(starts)}")
    for i in range(starts[0] + 1, len(lines)):
        if re.match(r"^\s*command:\s*\|\s*$", lines[i]):
            return block_at(lines, i)
        if re.match(r"^  \S", lines[i]):
            break
    raise SystemExit(f"{DEFAULTS}: {key} has no command block")


def run(body, payload, home):
    """Run a hook body through sh with HOME pointed at a throwaway directory."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env["HOME"] = home
    return subprocess.run(
        ["sh", "-c", body],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )


def denied(body, tool, tool_input, home, sid="s1"):
    """True when the guard denies the call. Fails loudly on anything but 0 or 2."""
    if isinstance(tool_input, str):
        tool_input = {"command": tool_input}
    proc = run(body, {"session_id": sid, "tool_name": tool, "tool_input": tool_input}, home)
    if proc.returncode not in (0, 2):
        raise SystemExit(f"guard exited {proc.returncode} for {tool_input!r}: {proc.stderr[:300]}")
    if proc.returncode == 2 and "BLOCKED" not in proc.stderr:
        raise SystemExit(f"exit 2 without the guard message for {tool_input!r}: {proc.stderr[:300]}")
    return proc.returncode == 2


def prompt(body, text, home, sid="s1"):
    proc = run(body, {"session_id": sid, "hook_event_name": "UserPromptSubmit", "prompt": text}, home)
    if proc.returncode != 0 or proc.stdout:
        raise SystemExit(f"prompt hook must exit 0 silently: rc={proc.returncode} out={proc.stdout!r} err={proc.stderr!r}")


def stop(body, home, sid="s1"):
    proc = run(body, {"session_id": sid, "hook_event_name": "Stop"}, home)
    if proc.returncode != 0:
        raise SystemExit(f"stop hook exited {proc.returncode}: {proc.stderr[:300]}")


def main():
    failures = []
    bodies = {key: extract(key) for key in (GUARD, PROMPT, CLEAR)}

    # Each body is embedded in a `python3 -c "..."` shell string: a bare double
    # quote would close it early, and sh would expand a backtick or dollar sign.
    for key, body in bodies.items():
        inner = body.split("\n")[1:-1]
        for ch, what in ((DQ, "double quote"), (BT, "backtick"), (DOLLAR, "dollar sign")):
            if any(ch in line for line in inner):
                failures.append(f"{key}: body contains a bare {what}")

    guard, on_prompt, on_stop = bodies[GUARD], bodies[PROMPT], bodies[CLEAR]

    with tempfile.TemporaryDirectory() as home:
        cases = [(t, i, f"{lbl} (HOME={home})") for t, i, lbl in [
            ("Bash", f"HOME={home} claude -p hi", "HOME set to the real home"),
        ]]
        for tool, tool_input, label in ALLOW + cases:
            if denied(guard, tool, tool_input, home):
                failures.append(f"false positive - {label}")
        for tool, tool_input, label in BLOCK + ALWAYS_BLOCK:
            if not denied(guard, tool, tool_input, home):
                failures.append(f"not denied - {label}")
        for tool, tool_input, label in KNOWN_GAPS:
            if denied(guard, tool, tool_input, home):
                failures.append(f"KNOWN_GAPS case now denies - {label}. If intended, move it into BLOCK.")

        legacy_fp = [lbl for tool, inp, lbl in ALLOW if denied_legacy(inp, home)]
        if not legacy_fp:
            failures.append("control: substring scanner cleared ALLOW, so it cannot fail")

        probe = ("Bash", f"security find-generic-password -s {FAKE_ITEM}")
        allowance = pathlib.Path(home, ".claude", "keychain-allowance", "s1")

        # A prompt without the phrase grants nothing.
        prompt(on_prompt, "please look up the token in the keychain", home)
        if not denied(guard, *probe, home):
            failures.append("allowance: granted without the phrase")

        # The phrase, in any case or spacing, grants this session only.
        prompt(on_prompt, "Fine - Allow   Keychain\nAccess for this one.", home)
        if not allowance.is_file():
            failures.append("allowance: phrase did not record an allowance")
        for tool, tool_input, label in BLOCK:
            if denied(guard, tool, tool_input, home):
                failures.append(f"allowance: still denied with the phrase - {label}")
        for tool, tool_input, label in ALWAYS_BLOCK:
            if not denied(guard, tool, tool_input, home):
                failures.append(f"allowance: allowance path writable by the agent - {label}")
        if not denied(guard, *probe, home, sid="s2"):
            failures.append("allowance: leaked to another session")
        if not denied(guard, *probe, home, sid=""):
            failures.append("allowance: applies with no session id")

        # The turn ends: Stop clears it.
        stop(on_stop, home)
        if allowance.exists() or not denied(guard, *probe, home):
            failures.append("allowance: survived Stop")

        # The next prompt without the phrase revokes a leftover allowance.
        prompt(on_prompt, "allow keychain access", home)
        prompt(on_prompt, "now do something else", home)
        if allowance.exists() or not denied(guard, *probe, home):
            failures.append("allowance: survived a prompt without the phrase")

        # A crafted session id cannot write outside the allowance directory.
        prompt(on_prompt, "allow keychain access", home, sid="../../escape")
        if pathlib.Path(home, "escape").exists() or pathlib.Path(home, ".claude", "escape").exists():
            failures.append("allowance: session id escaped the allowance directory")

        # Malformed input never blocks a prompt or a stop.
        for body, name in ((on_prompt, PROMPT), (on_stop, CLEAR)):
            proc = subprocess.run(["sh", "-c", body], input="not json", capture_output=True,
                                  text=True, timeout=30, env={**os.environ, "HOME": home})
            if proc.returncode != 0:
                failures.append(f"{name}: malformed input exited {proc.returncode}")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(
        f"keychain_guard OK: {len(BLOCK) + len(ALWAYS_BLOCK)} denied + {len(ALLOW) + 1} allowed + "
        f"{len(KNOWN_GAPS)} known gaps; allowance granted only by the prompt phrase, per session, "
        f"cleared on Stop; substring control fails {len(legacy_fp)} of the allowed cases"
    )
    return 0


def denied_legacy(tool_input, home):
    if isinstance(tool_input, str):
        tool_input = {"command": tool_input}
    return run(LEGACY, {"tool_input": tool_input}, home).returncode == 2


if __name__ == "__main__":
    sys.exit(main())
