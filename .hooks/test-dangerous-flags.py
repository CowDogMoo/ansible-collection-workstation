#!/usr/bin/env python3
"""Test the dangerous_flags PreToolUse hook in every file that ships it.

The hook must block real bypass attempts - including ones hidden behind shell
wrappers or assembled at runtime by xargs or command substitution - while
leaving alone any command that merely searches for or documents the flag.

The detector body is extracted from the shipped YAML and executed through `sh`
exactly as the hook harness runs it, so block-scalar embedding and shell
escaping are covered too. Positive controls prove the matrices can fail.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
MARKER = "DANGEROUS ="

SHIPPED = {
    "claude_code": "roles/claude_code/defaults/main.yml",
    "antigravity": "roles/antigravity/defaults/main.yml",
    "host_vars": "playbooks/workstation/host_vars/MacBook-Pro-4/main.yml",
}

G = "git"
NV = "--no-verify"
NG = "--no-gpg-sign"
NPR = "--no-post-rewrite"
BS = chr(92)
SQ = chr(39)
BT = chr(96)
TAB = chr(9)

# (command, label) - every one of these must be blocked.
BYPASS = [
    (f'{G} commit -m "x" {NV}', "direct"),
    (f"{G} commit {NV} -F -", "stdin commit"),
    (f"/usr/bin/{G} commit {NV}", "absolute path"),
    (f"{G} commit -n -m x", "short form"),
    (f"{G} push --force && {G} commit {NV}", "second clause"),
    (f"echo x | {G} commit {NV} -F -", "after a pipe"),
    (f"{G} commit {NG} -m x", "gpg flag"),
    (f"{G} rebase {NPR} main", "post-rewrite flag"),
    (f"GIT_DIR=.{G} {G} commit {NV}", "env assignment prefix"),
    (f'bash -c "{G} commit {NV}"', "bash -c"),
    (f"sh -c '{G} commit {NV}'", "sh -c"),
    (f'bash -lc "{G} commit {NV}"', "bash -lc"),
    (f"env {G} commit {NV}", "env"),
    (f"sudo {G} commit {NV}", "sudo"),
    (f"sudo -u dev {G} commit {NV}", "sudo with option"),
    (f"nohup {G} commit {NV}", "nohup"),
    (f"timeout 5 {G} commit {NV}", "timeout"),
    (f'sudo -u dev bash -c "{G} commit {NV}"', "nested wrappers"),
    (f'echo "{NV}" | xargs {G} commit', "xargs from stdin"),
    (f"echo {NV} | xargs -I{{}} {G} commit {{}}", "xargs -I placeholder"),
    (f"{G} commit $(echo {NV})", "command substitution"),
    (f"{G} commit {NV}; echo hi", "after a semicolon"),
    (f"({G} commit {NV})", "inside a subshell"),
    (f"{BS}{G} commit {NV}", "backslash-escaped name"),
    (f'{G} commit -m ";" {NV}', "quoted semicolon argument"),
    (f'"{G}" commit {NV}', "quoted name"),
    (f"{G}{TAB}commit{TAB}{NV}", "tab separated"),
    (f'eval "{G} commit {NV}"', "eval with a quoted payload"),
    (f"eval {G} commit {NV}", "eval with bare arguments"),
    (f"exec {G} commit {NV}", "exec"),
    (f"{G} commit --no-verif{SQ}y{SQ}", "quote spliced into the flag"),
    (f'{G} commit --no-ver"ify"', "double quote spliced into the flag"),
    (f"g{SQ}i{SQ}t commit {NV}", "quote spliced into the command name"),
    (f"g{BS}it commit {NV}", "escape spliced into the command name"),
    (f"{G} commit ${SQ}{NV}{SQ}", "ANSI-C quoted flag"),
    (f'{G} commit $"{NV}"', "locale-quoted flag"),
    (f"{G} commit ${SQ}--no-{SQ}verify", "ANSI-C quoted flag fragment"),
    (f"bash -c {SQ}{G} commit $(echo {NV}){SQ}", "wrapper wrapping a substitution"),
    (f"sh -c {SQ}echo {NV} | xargs {G} commit{SQ}", "wrapper wrapping an xargs pipe"),
    (f"eval {SQ}{G} commit $(echo {NV}){SQ}", "eval wrapping a substitution"),
    (f"{BT}{G} commit {NV}{BT}", "backtick command substitution"),
    (f"echo {BT}{G} commit {NV}{BT}", "backtick substitution as an argument"),
    (f'x={NV}; {G} commit "$x"', "flag stored in a variable"),
    (f"x={SQ}{G} commit {NV}{SQ}; eval \"$x\"", "whole command stored in a variable"),
    (f'python3 -c "import subprocess; subprocess.run([{SQ}{G}{SQ},{SQ}commit{SQ},{SQ}{NV}{SQ}])"',
     "python -c payload"),
    (f"perl -e {SQ}system(\"{G} commit {NV}\"){SQ}", "perl -e payload"),
    (f'python3 -uc "import subprocess; subprocess.run([{SQ}{G}{SQ},{SQ}commit{SQ},{SQ}{NV}{SQ}])"',
     "python bundled -uc payload"),
    (f"perl -we {SQ}system(\"{G} commit {NV}\"){SQ}", "perl bundled -we payload"),
    # These four are deliberately NOT in any wrapper list: the trailing-argv rule
    # must cover exec-style wrappers generically, not by enumeration.
    (f"flock /tmp/{G}.lock {G} commit {NV}", "flock, an unenumerated exec wrapper"),
    (f"chrt -f 10 {G} commit {NV}", "chrt, an unenumerated exec wrapper"),
    (f"ionice -c3 {G} commit {NV}", "ionice, an unenumerated exec wrapper"),
    (f"runuser -u dev -- {G} commit {NV}", "runuser, an unenumerated exec wrapper"),
    (f"echo {SQ}{G} commit {NV}{SQ} | sh", "script piped into sh"),
    (f"echo {SQ}{G} commit {NV}{SQ} | bash", "script piped into bash"),
    (f"printf {SQ}%s{SQ} {SQ}{G} commit {NV}{SQ} | sh", "printf piped into sh"),
]

# (command, label) - none of these may be blocked.
FALSEPOS = [
    (f"rg -n -- '{NV}' --hidden -g '!.{G}' .", "ripgrep search"),
    (f"grep -rn '{NV}' roles/", "grep search"),
    (f"echo 'never use {NV}' >> README.md", "documenting the flag"),
    (f"echo '{G} commit {NV} is banned' >> R.md", "doc quoting a whole command"),
    (f"{G} commit -m 'note about {NV} policy'", "flag named inside a message"),
    (f"sed -i '' 's/a/b/' roles/{G}hub/x.yml", "path containing the name"),
    (f"{G} status --short", "plain status"),
    (f"{G} log --oneline -n 5", "legitimate -n"),
    ("ls -la", "unrelated command"),
    ("echo hello world", "no mention at all"),
    (f"eval \"echo '{G} commit {NV}'\"", "eval echoing a doc line"),
    (f'bash -c "echo {SQ}{G} commit {NV} is banned{SQ}"', "doc line inside a wrapper"),
    (f'bash -c "rg -n -- {SQ}{NV}{SQ} ."', "search inside a wrapper"),
    (f'python3 -c "print({SQ}never use {NV}{SQ})"', "python printing a doc line"),
    (f'python3 -uc "print({SQ}never use {NV}{SQ})"', "bundled-option python printing a doc line"),
    (f"{G} log --oneline && echo {SQ}{NV}{SQ}", "unrelated clauses, not one invocation"),
    (f"{G} status && echo {NV} >> notes.md", "status then documenting the flag"),
    (f"rg {NV} . ; {G} status", "search then an unrelated status"),
    ("cat README.md | sh", "unrelated pipe into a shell"),
]

# Positive controls. LEGACY is the pre-fix substring scanner: it must fail the
# false-positive matrix. NAIVE only inspects each clause's command word: it must
# fail the bypass matrix. Without these, a matrix that cannot fail proves nothing.
_LEGACY_BODY = """
import json, sys, re
d = json.load(sys.stdin)
cmd = d.get('tool_input', {}).get('command', '')
if 'GG' not in cmd:
    sys.exit(0)
f = next((x for x in ['VV', 'PP', 'RR'] if x in cmd), None)
if f:
    sys.stderr.write('BLOCKED: Cannot use ' + f)
    sys.exit(2)
sys.exit(0)
"""

_NAIVE_BODY = """
import json, sys, shlex
d = json.load(sys.stdin)
cmd = d.get('tool_input', {}).get('command', '')
if 'GG' not in cmd:
    sys.exit(0)
try:
    toks = shlex.split(cmd)
except ValueError:
    toks = cmd.split()
clauses, cur = [], []
for t in toks:
    if t in ('&&', '||', '|', ';', '&'):
        clauses.append(cur)
        cur = []
    else:
        cur.append(t)
clauses.append(cur)
hit = None
for c in clauses:
    if not c or c[0].split('/')[-1] != 'GG':
        continue
    for f in ['VV', 'PP', 'RR']:
        if f in c[1:]:
            hit = f
if hit:
    sys.stderr.write('BLOCKED: Cannot use ' + hit)
    sys.exit(2)
sys.exit(0)
"""


def _control(body: str) -> str:
    filled = body.replace("GG", G).replace("VV", NV).replace("PP", NG).replace("RR", NPR)
    return "python3 -c " + chr(34) + filled + chr(34)


LEGACY = _control(_LEGACY_BODY)
NAIVE = _control(_NAIVE_BODY)


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
    return "\n".join(x[cut:] for x in body)


def extract(rel):
    """Pull the one `command:` block scalar holding the detector."""
    lines = (REPO / rel).read_text().split("\n")
    blocks = [
        block_at(lines, i)
        for i, line in enumerate(lines)
        if re.match(r"^\s*command:\s*\|\s*$", line)
    ]
    found = [b for b in blocks if MARKER in b]
    if len(found) != 1:
        raise SystemExit(f"{rel}: expected 1 detector block, found {len(found)}")
    return found[0]


def run_hook(body, cmd):
    """Execute the hook the way the harness does. True means it blocked."""
    json_protocol = "toolCall" in body
    payload = (
        {"toolCall": {"args": {"CommandLine": cmd}}}
        if json_protocol
        else {"tool_input": {"command": cmd}}
    )
    proc = subprocess.run(
        ["sh", "-c", body],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if json_protocol:
        try:
            return json.loads(proc.stdout.strip())["decision"] == "deny"
        except (ValueError, KeyError) as exc:
            raise SystemExit(f"hook returned no decision for {cmd!r}: {exc}")
    # `sh` also exits 2 on a syntax error, which would otherwise read as a block.
    if proc.returncode not in (0, 2):
        raise SystemExit(f"hook exited {proc.returncode} for {cmd!r}: {proc.stderr[:200]}")
    if proc.returncode == 2 and "Cannot use" not in proc.stderr:
        raise SystemExit(f"exit 2 without the hook message for {cmd!r}: {proc.stderr[:200]}")
    return proc.returncode == 2


def main():
    failures = []
    bodies = {name: extract(rel) for name, rel in SHIPPED.items()}

    # The detector is embedded in a `python3 -c "..."` shell string, so a bare
    # double quote anywhere in it would close that string early.
    for name, body in bodies.items():
        tail = body[body.index(MARKER):].split(chr(10))
        # the lone trailing quote is the legitimate close of `python3 -c "`
        detector = chr(10).join(x for x in tail if x.strip() != chr(34))
        for ch, what in ((chr(34), "double quote"), (chr(96), "backtick")):
            if ch in detector:
                failures.append(f"{name}: detector body contains a bare {what}")

    for name, body in bodies.items():
        for cmd, label in BYPASS:
            if not run_hook(body, cmd):
                failures.append(f"{name}: bypass not blocked - {label}")
        for cmd, label in FALSEPOS:
            if run_hook(body, cmd):
                failures.append(f"{name}: false positive - {label}")

    for cmd, label in BYPASS + FALSEPOS:
        verdicts = {name: run_hook(body, cmd) for name, body in bodies.items()}
        if len(set(verdicts.values())) != 1:
            failures.append(f"copies disagree on {label}: {verdicts}")

    legacy_fp = [lbl for cmd, lbl in FALSEPOS if run_hook(LEGACY, cmd)]
    naive_bp = [lbl for cmd, lbl in BYPASS if not run_hook(NAIVE, cmd)]
    if not legacy_fp:
        failures.append("control: substring scanner cleared FALSEPOS, so it cannot fail")
    if not naive_bp:
        failures.append("control: naive tokenizer cleared BYPASS, so it cannot fail")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(
        f"dangerous_flags OK: {len(BYPASS)} bypass + {len(FALSEPOS)} documentation "
        f"cases across {len(bodies)} shipped copies; controls fail as expected "
        f"(substring scanner on {len(legacy_fp)}, naive tokenizer on {len(naive_bp)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
