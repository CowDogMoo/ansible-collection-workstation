#!/usr/bin/python3
"""Local PreToolUse gate for the first mate's Bash calls (captain-private, not upstream).

Closes two gaps fm-spawn.sh leaves open:

1. Dispatch conformance. When config/crew-dispatch.json exists, a crewmate or
   scout spawn must launch exactly a profile the file declares: same harness,
   and the profile's model and effort whenever the profile sets them. fm-spawn's
   own backstop only checks that *some* --harness was passed, so a bare
   `--harness claude` used to slip through. A captain-directed per-task choice
   still works through `--dispatch-override "<reason>"`, which fm-spawn records
   in the task meta.

2. Ship harness allowlist. When config/ship-harnesses exists, a ship spawn and a
   scout-to-ship promotion may only use a harness listed there. These are the
   harnesses proven to follow the captain's commit/PR rules (squad_commit,
   squad_pr, no --no-verify, no AI attribution). --dispatch-override does NOT
   bypass this check.

Relaunches and secondmate spawns are left to fm-spawn. Anything that is not an
fm-spawn.sh / fm-promote.sh call passes untouched. Deny = exit 2 + stderr.
"""
import json
import os
import shlex
import sys

KNOWN_HARNESSES = {
    "claude", "codex", "opencode", "pi", "pi-signed", "grok", "kimi", "cursor",
    "omp", "agy", "muse", "gemini", "rovo", "devin", "commandcode", "polytoken",
    "cortex", "kiro", "hermes",
}
VALUE_FLAGS = {
    "--harness", "--model", "--effort", "--dispatch-override", "--hermes-profile",
    "--account", "--backend", "--mode", "--yolo", "--branch-prefix",
    "--base-branch", "--upstream-consent", "--traceparent",
}
SEPARATORS = {"&&", "||", ";", "|", "&", "\n", "(", ")"}
WRAPPERS = {"bash", "sh", "zsh"}


def deny(msg):
    sys.stderr.write("fm-dispatch-gate: " + msg + "\n")
    sys.exit(2)


def tokenize(cmd):
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|()")
    lex.whitespace_split = True
    lex.whitespace = " \t\r"
    lex.commenters = ""
    out = []
    for tok in lex:
        if "\n" in tok:
            parts = tok.split("\n")
            for i, p in enumerate(parts):
                if p:
                    out.append(p)
                if i < len(parts) - 1:
                    out.append("\n")
        else:
            out.append(tok)
    return out


def clauses(cmd, depth=0):
    """Yield token lists, one per simple command, looking one level into sh -c."""
    try:
        toks = tokenize(cmd)
    except ValueError:
        # Unparsable (e.g. unbalanced quotes). Only matters if it names a gated script.
        if "fm-spawn.sh" in cmd or "fm-promote.sh" in cmd:
            deny("could not parse a command that calls fm-spawn.sh/fm-promote.sh; "
                 "run it as a plain command with literal flags")
        return
    cur = []
    for t in toks + [";"]:
        if t in SEPARATORS or all(c in ";&|()" for c in t):
            if cur:
                yield cur
                if depth == 0:
                    base = os.path.basename(cur[0])
                    if base in WRAPPERS and "-c" in cur[1:]:
                        i = cur.index("-c")
                        if i + 1 < len(cur):
                            for sub in clauses(cur[i + 1], depth + 1):
                                yield sub
            cur = []
        else:
            cur.append(t)


PREFIXES = {"env", "exec", "command", "nohup", "time", "bash", "sh", "zsh"}


def find_call(tokens, script):
    """Return the args if this simple command *runs* script (not merely mentions it)."""
    i = 0
    while i < len(tokens):
        t = tokens[i]
        head = t.split("=", 1)[0]
        if "=" in t and head.replace("_", "a").isalnum() and not head[0].isdigit():
            i += 1  # leading VAR=value assignment
            continue
        if os.path.basename(t) in PREFIXES:
            i += 1
            while i < len(tokens) and tokens[i].startswith("-") and tokens[i] != "-c":
                i += 1
            continue
        break
    if i < len(tokens) and os.path.basename(tokens[i]) == script:
        return tokens[i + 1:]
    return None


def parse_spawn(args):
    flags, pos = {}, []
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            if "=" in a:
                k, v = a.split("=", 1)
                flags[k] = v
            elif a in VALUE_FLAGS:
                if i + 1 >= len(args):
                    deny("%s needs a value" % a)
                flags[a] = args[i + 1]
                i += 1
            else:
                flags[a] = True
        else:
            pos.append(a)
        i += 1
    return flags, pos


def load_profiles(path):
    try:
        with open(path) as f:
            cfg = json.load(f)
    except Exception as e:  # malformed config is an actionable error, never selected around
        deny("config/crew-dispatch.json is unreadable or malformed (%s); fix it before spawning" % e)

    def as_list(v):
        if isinstance(v, dict):
            return [v]
        if isinstance(v, list):
            return [p for p in v if isinstance(p, dict)]
        return []

    profiles = []
    for rule in cfg.get("rules") or []:
        if isinstance(rule, dict):
            profiles.extend(as_list(rule.get("use")))
    profiles.extend(as_list(cfg.get("default")))
    return profiles


def profile_matches(p, harness, model, effort):
    if p.get("harness") != harness:
        return False
    if p.get("model") is not None and p.get("model") != model:
        return False
    if p.get("effort") is not None and p.get("effort") != effort:
        return False
    return True


def fmt(h, m, e):
    s = "--harness %s" % h
    if m:
        s += " --model %s" % m
    if e:
        s += " --effort %s" % e
    return s


def ship_harnesses(home):
    path = os.path.join(home, "config", "ship-harnesses")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return {ln.split("#", 1)[0].strip() for ln in f if ln.split("#", 1)[0].strip()}


def check_spawn(args, home):
    flags, pos = parse_spawn(args)
    if flags.get("--secondmate") or flags.get("--relaunch"):
        return
    kind = "scout" if flags.get("--scout") else "ship"

    # Harness: --harness, else a positional adapter after <id> <project> (or after id=repo pairs).
    harness = flags.get("--harness")
    raw_launch = False
    if harness is None:
        extra = [p for p in pos if "=" not in p] if any("=" in p for p in pos) else pos[2:]
        if extra:
            harness = extra[0]
    if harness is not None and harness not in KNOWN_HARNESSES:
        raw_launch = True
    model = flags.get("--model")
    effort = flags.get("--effort")
    override = flags.get("--dispatch-override")
    override = override if isinstance(override, str) and override.strip() else None

    allowed = ship_harnesses(home)
    if kind == "ship" and allowed is not None:
        if raw_launch or harness not in allowed:
            deny("ship tasks may only run on a harness that enforces the captain's commit/PR "
                 "rules (squad_commit, squad_pr, no --no-verify, no AI attribution). "
                 "Allowed now: %s (config/ship-harnesses). '%s' is not listed; pick the "
                 "matched rule's next profile on an allowed harness. --dispatch-override "
                 "does not bypass this." % (", ".join(sorted(allowed)) or "none", harness))

    dispatch = os.path.join(home, "config", "crew-dispatch.json")
    if not os.path.isfile(dispatch) or override:
        return
    if harness is None:
        return  # fm-spawn's own backstop refuses a missing harness with its own message
    profiles = load_profiles(dispatch)
    if raw_launch or not any(profile_matches(p, harness, model, effort) for p in profiles):
        same = [p for p in profiles if p.get("harness") == harness]
        hint = "; ".join(sorted({fmt(p.get("harness"), p.get("model"), p.get("effort")) for p in same})) or "none"
        deny("%s matches no profile in config/crew-dispatch.json. Resolve the task's rule "
             "(AGENTS.md section 4, quota-array-dispatch) and pass that profile's harness, "
             "model and effort exactly. Declared %s profiles: %s. For a captain-directed "
             "per-task choice, add --dispatch-override \"<reason>\"."
             % (fmt(harness, model, effort), harness, hint))


def check_promote(args, home):
    allowed = ship_harnesses(home)
    if allowed is None:
        return
    pos = [a for a in args if not a.startswith("--")]
    if not pos:
        return
    task = pos[0]
    meta = os.path.join(os.environ.get("FM_STATE_OVERRIDE") or os.path.join(home, "state"), task + ".meta")
    harness = None
    try:
        with open(meta) as f:
            for ln in f:
                if ln.startswith("harness="):
                    harness = ln.strip().split("=", 1)[1]
    except OSError:
        return  # fm-promote reports a missing task itself
    if harness and harness not in allowed:
        deny("cannot promote %s to a ship: its worker runs on '%s', which is not in "
             "config/ship-harnesses (%s). Re-dispatch the ship on an allowed harness instead."
             % (task, harness, ", ".join(sorted(allowed))))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if "fm-spawn.sh" not in cmd and "fm-promote.sh" not in cmd:
        return 0
    home = os.environ.get("FM_HOME") or os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    for toks in clauses(cmd):
        spawn = find_call(toks, "fm-spawn.sh")
        if spawn is not None:
            if "--help" in spawn or "-h" in spawn:
                continue
            check_spawn(spawn, home)
        promote = find_call(toks, "fm-promote.sh")
        if promote is not None:
            check_promote(promote, home)
    return 0


if __name__ == "__main__":
    sys.exit(main())
