#!/usr/bin/env python3
"""Test the claude_code forbidden_content hook's squad-only rule.

Commits and pull request titles and bodies come only from squad_commit and
squad_pr. The hook must deny every command an agent would actually reach for to
write that text itself - a raw commit, an amend, gh or gh-axi pr create/edit,
gh api writes to a pulls endpoint - while allowing squad_commit, squad_pr, and
read-only git and gh commands, plus the attribution guard it already carried.

The one exemption is `git commit --no-edit` while a merge is in progress: it is
how the no-mistakes pipeline's agent concludes a merge-strategy conflict, and it
carries git's own message rather than hand-written text. It is exercised in a
real repository with and without MERGE_HEAD.

KNOWN_GAPS records what is deliberately not caught. Each has to be constructed
on purpose; they are asserted to pass so the boundary stays explicit.

The detector body is extracted from the shipped YAML and executed through `sh`
exactly as the hook harness runs it, so block-scalar embedding and shell
escaping are covered too.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
SHIPPED = "roles/claude_code/defaults/main.yml"
MARKER = "SQUAD_ONLY ="

G = "git"
SQ = chr(39)
DQ = chr(34)
BT = chr(96)
PULLS = "repos/{owner}/{repo}/pulls"

# (command, label) - every one of these must be denied.
DENY = [
    (f"{G} commit -m {SQ}fix: thing{SQ}", "raw commit"),
    (f"{G} commit -F /tmp/msg", "commit from a file"),
    (f"printf {SQ}fix{SQ} | {G} commit -F -", "commit from a pipe"),
    (f"{G} commit", "editor commit"),
    (f"{G} commit --amend --no-edit", "amend without a merge"),
    (f"{G} commit --amend -m x", "amend with a message"),
    (f"{G} commit --no-edit", "--no-edit with no merge in progress"),
    (f"{G} commit -am x", "commit all"),
    (f"{G} -C /tmp commit -m x", "-C before the subcommand"),
    (f"{G} -c user.name=x commit -m x", "-c before the subcommand"),
    (f"/usr/bin/{G} commit -m x", "absolute path"),
    (f"GIT_EDITOR=true {G} commit", "env prefix"),
    (f"sudo {G} commit -m x", "sudo"),
    (f"{G} add -A && {G} commit -m x", "after git add"),
    (f"squad_commit; {G} commit --amend -m x", "amend after squad_commit"),
    (f"({G} commit -m x)", "inside a subshell"),
    (f'bash -c "{G} commit -m x"', "bash -c"),
    (f'eval "{G} commit -m x"', "eval"),
    (f"{G} commit-tree HEAD^{{tree}} -m x", "commit-tree"),
    ("gh pr create --title x --body y", "gh pr create"),
    ("gh pr create --fill", "gh pr create --fill"),
    ("gh pr new -t x -b y", "gh pr new"),
    ("gh pr create -t x -F body.md", "gh pr create from a file"),
    ("gh pr edit 12 --title x", "gh pr edit title"),
    ("gh pr edit --body y", "gh pr edit body"),
    ("gh pr edit 12 -b y", "gh pr edit short body"),
    ("gh pr edit 12 --body-file b.md", "gh pr edit body file"),
    ("gh pr edit 12 --title=x", "gh pr edit title with ="),
    ("gh-axi pr create --title x --body y", "gh-axi pr create"),
    ("gh-axi pr edit 12 --body y", "gh-axi pr edit body"),
    (f"gh api {PULLS} -f title=x -f head=b -f base=main", "gh api fields default to POST"),
    (f"gh api -X POST {PULLS} --input body.json", "gh api -X POST"),
    (f"gh api --method PATCH {PULLS}/12 -f body=y", "gh api PATCH pull"),
    (f"gh api /{PULLS}/12 -X PATCH -f title=x", "gh api leading slash"),
    (f"gh-axi api POST /{PULLS} --field title=x", "gh-axi api POST"),
    (f"gh-axi api PATCH /{PULLS}/12 --raw-field body=y", "gh-axi api PATCH"),
    ("gh api graphql -f query=" + SQ + "mutation { updatePullRequest(input: {}) { clientMutationId } }" + SQ,
     "graphql updatePullRequest"),
    (f'bash -c "gh pr edit 12 --body y"', "gh inside a wrapper"),
]

# (command, label) - none of these may be denied.
ALLOW = [
    ("squad_commit", "squad_commit"),
    ("squad_pr", "squad_pr"),
    ("cd /tmp && squad_commit", "squad_commit after cd"),
    (f"{G} add -A && squad_commit", "squad_commit after git add"),
    ("squad_commit && squad_pr", "squad_commit then squad_pr"),
    (f"{G} ds | squad_gen commit", "previewing the generated message"),
    (f"{G} status --short", "git status"),
    (f"{G} log --oneline -n 5", "git log"),
    (f"{G} diff main...HEAD", "git diff"),
    (f"{G} show HEAD --stat", "git show"),
    (f"{G} log -1 --format=%B", "reading a commit message"),
    (f"{G} rebase --continue", "rebase --continue"),
    (f"{G} merge --continue", "merge --continue"),
    (f"{G} push -u origin HEAD", "git push"),
    (f"{G} add -A", "git add"),
    (f"{G} -C /tmp status", "git -C status"),
    ("gh pr view 12", "gh pr view"),
    ("gh pr view --json title,body", "gh pr view json"),
    ("gh pr list --state open", "gh pr list"),
    ("gh pr checks 12", "gh pr checks"),
    ("gh pr diff 12", "gh pr diff"),
    ("gh pr edit 12 --add-label bug", "gh pr edit label only"),
    ("gh pr ready 12", "gh pr ready"),
    ("gh run list", "gh run list"),
    ("gh-axi pr view 12", "gh-axi pr view"),
    ("gh-axi pr checks 12", "gh-axi pr checks"),
    (f"gh api {PULLS}", "gh api GET pulls"),
    (f"gh api {PULLS}/12 --jq .body", "gh api GET one pull"),
    (f"gh api -X GET {PULLS} -f state=open", "gh api explicit GET with fields"),
    (f"gh api -X POST {PULLS}/12/comments -f body=x", "gh api review comment"),
    (f"gh api -X PUT {PULLS}/12/merge", "gh api merge"),
    ("gh-axi api /" + PULLS, "gh-axi api GET pulls"),
    (f"rg -n {SQ}{G} commit{SQ} roles/", "searching for git commit"),
    (f"rg -n {DQ}gh pr create{DQ} .", "searching for gh pr create"),
    (f"echo {SQ}never run {G} commit by hand{SQ} >> README.md", "documenting the rule"),
    (f'bash -c "echo {SQ}{G} commit{SQ}"', "doc line inside a wrapper"),
    (f'python3 -c "print({SQ}{G} commit{SQ})"', "python printing a doc line"),
    ("ls -la", "unrelated command"),
]

# Deliberately not caught: each has to be constructed to slip past.
KNOWN_GAPS = [
    (f"{G} ci -m x", "git alias for commit"),
    (f"{BT}echo {G}{BT} commit -m x", "backtick substitution"),
    (f"$(echo {G}) commit -m x", "command substitution"),
    (f"bash -c {SQ}bash -c {DQ}{G} commit -m x{DQ}{SQ}", "two levels of wrapping"),
    (f"echo {SQ}{G} commit -m x{SQ} | sh", "script piped into sh"),
    ("curl -X PATCH https://api.github.com/repos/o/r/pulls/1 -d @b.json", "curl to the API"),
    ("gh api -X PATCH repos/{owner}/{repo}/issues/12 -f body=y", "PR body through the issues endpoint"),
]

# Attribution must still be blocked on commands the squad rule does not deny.
ATTRIBUTION = [
    ("gh pr comment 12 --body " + SQ + "Generated with Claude Code" + SQ, "attribution in a PR comment"),
    (f"{G} tag -a v1 -m {SQ}Co-Authored-By: Claude{SQ}", "attribution in a tag"),
]


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
    """Pull the one `command:` block scalar holding the squad-only rule."""
    lines = (REPO / rel).read_text().split("\n")
    blocks = [
        block_at(lines, i)
        for i, line in enumerate(lines)
        if re.match(r"^\s*command:\s*\|\s*$", line)
    ]
    found = [b for b in blocks if MARKER in b]
    if len(found) != 1:
        raise SystemExit(f"{rel}: expected 1 squad-only block, found {len(found)}")
    return found[0]


def run_hook(body, cmd, cwd):
    """Run the hook as Claude Code does. Returns (exit code, stderr)."""
    proc = subprocess.run(
        ["sh", "-c", body],
        input=json.dumps({"tool_input": {"command": cmd}, "cwd": cwd}),
        capture_output=True,
        text=True,
        timeout=30,
    )
    # `sh` also exits 2 on a syntax error, which would otherwise read as a block.
    if proc.returncode not in (0, 2):
        raise SystemExit(f"hook exited {proc.returncode} for {cmd!r}: {proc.stderr[:300]}")
    if proc.returncode == 2 and "BLOCKED" not in proc.stderr:
        raise SystemExit(f"exit 2 without the hook message for {cmd!r}: {proc.stderr[:300]}")
    return proc.returncode, proc.stderr


def git(repo, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    return subprocess.run([G, "-C", repo, *args], capture_output=True, text=True, env=env)


def conflicted_merge(root):
    """A repository stopped in a conflicted merge, so MERGE_HEAD exists."""
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "commit.gpgsign", "false")
    pathlib.Path(repo, "f").write_text("base\n")
    git(repo, "add", "f")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "checkout", "-q", "-b", "side")
    pathlib.Path(repo, "f").write_text("side\n")
    git(repo, "commit", "-q", "-am", "side")
    git(repo, "checkout", "-q", "main")
    pathlib.Path(repo, "f").write_text("main\n")
    git(repo, "commit", "-q", "-am", "main")
    git(repo, "merge", "side")
    if git(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode != 0:
        raise SystemExit("fixture: merge did not stop with MERGE_HEAD")
    return repo


def main():
    failures = []
    body = extract(SHIPPED)

    # The body is embedded in a `python3 -c "..."` shell string: a bare double
    # quote would close it early and a backtick or `$(` would be substituted.
    detector = chr(10).join(x for x in body.split(chr(10))[1:] if x.strip() != DQ)
    for bad, what in ((DQ, "double quote"), (BT, "backtick"), ("$(", "command substitution")):
        if bad in detector:
            failures.append(f"hook body contains a bare {what}")

    with tempfile.TemporaryDirectory() as root:
        plain = os.path.join(root, "plain")
        os.makedirs(plain)

        for cmd, label in DENY:
            rc, err = run_hook(body, cmd, plain)
            if rc != 2:
                failures.append(f"not denied - {label}")
            elif "squad_commit or squad_pr" not in err:
                failures.append(f"deny message does not name squad_commit or squad_pr - {label}")
        for cmd, label in ALLOW:
            rc, err = run_hook(body, cmd, plain)
            if rc != 0:
                failures.append(f"false positive - {label}: {err.strip()[:120]}")
        for cmd, label in KNOWN_GAPS:
            if run_hook(body, cmd, plain)[0] != 0:
                failures.append(f"KNOWN_GAPS case now denied - {label}. If intended, move it into DENY.")
        for cmd, label in ATTRIBUTION:
            rc, err = run_hook(body, cmd, plain)
            if rc != 2 or "forbidden content" not in err:
                failures.append(f"attribution not blocked - {label}")

        # The merge exemption: only the exact conclusion, only mid-merge.
        repo = conflicted_merge(root)
        merge_cases = [
            (f"{G} commit --no-edit", 0, "concluding a merge with --no-edit"),
            (f"{G} add f && {G} commit --no-edit", 0, "stage then conclude"),
            (f"{G} commit --no-edit -q", 0, "quiet conclusion"),
            (f"{G} commit -m x", 2, "hand-written message mid-merge"),
            (f"{G} commit --no-edit -m x", 2, "--no-edit plus a message mid-merge"),
            (f"{G} commit --amend --no-edit", 2, "amend mid-merge"),
        ]
        for cmd, want, label in merge_cases:
            if run_hook(body, cmd, repo)[0] != want:
                failures.append(f"merge exemption wrong - {label}")
        if run_hook(body, f"cd {repo} && {G} commit --no-edit", plain)[0] != 0:
            failures.append("merge exemption does not follow cd into the merging repo")
        if run_hook(body, f"{G} -C {repo} commit --no-edit", plain)[0] != 0:
            failures.append("merge exemption does not follow git -C into the merging repo")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(
        f"squad-only OK: {len(DENY)} denied + {len(ALLOW)} allowed + "
        f"{len(KNOWN_GAPS)} known gaps + {len(ATTRIBUTION)} attribution + merge exemption"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
