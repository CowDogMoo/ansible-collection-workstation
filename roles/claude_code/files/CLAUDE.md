# Global Claude Code Instructions

## CRITICAL: .claude Directory

**NEVER EVER commit the .claude directory or any of its contents to git!**

- The `.claude/` directory and its contents are personal/local configuration
- Always ensure `.claude/` is in `.gitignore`
- Never add, stage, or commit any files from `.claude/`
- If `.claude/` appears in git status as staged, immediately run `git restore --staged .claude/`

## Git Workflow

### Commits

Always use `fabric_commit` for commit messages:

```bash
fabric_commit
```

**NEVER EVER use --no-verify when committing or there will be dire consequences!**

- Never skip pre-commit hooks with `--no-verify` or `-n`
- Hooks are there for critical validation and security checks
- If a commit fails due to hooks, fix the issue and create a NEW commit
- Bypassing hooks can lead to broken builds, security vulnerabilities, and other serious problems

### Pull Requests

Always use `fabric_pr` for pull requests — both to **open** them and to **update** them. `fabric_pr` regenerates the title/body from the current `git diff main`, then creates the PR or, if one already exists for the branch, updates that PR in place.

```bash
fabric_pr
```

**The PR title and body must ALWAYS be `fabric_pr`'s generated output. NEVER hand-write or hand-edit them.**

- Any time the branch changes — after a **rebase, amend, new commits, or force-push** — the existing body is stale. Re-run `fabric_pr`; it regenerates from the new diff and updates the existing PR. This is the ONLY correct way to refresh a PR body.
- Do **not** run `gh pr edit --body "..."` (or `--title`) with text you wrote yourself, and do not "clean up", "correct", or "just fix" the body by hand. Substituting your own writing for fabric's output breaks this rule no matter how small the change. If the body needs to change, re-run `fabric_pr`.

**Format verification — after every `fabric_pr`:**

1. Check the PR with `gh pr view`.
2. Confirm the fabric output is clean: **no code fences (```)** in the title or body, and the **title is not duplicated** in the body.
3. If the output is malformed, the bug is in the fabric `pr` pattern or its `filter.sh` (`~/.config/fabric/patterns/pr/filter.sh`) — fix it at the source and re-run `fabric_pr`. Never patch the symptom by hand-editing the PR.

## Modern CLI Tools

Prefer these modern equivalents when installed — they are faster and have better defaults. They are **not** strict drop-ins; verify flags before substituting in scripts.

- `rg` (ripgrep) over `grep` — respects `.gitignore`, parallel
- `fd` over `find` — simpler positional syntax; for quick lookups, not complex `find -exec` chains
- `bat -pp` over `cat` — `-pp` disables paging and decoration for tool-friendly output
- `delta` for diffs — pipe `git diff` / `diff -u` through it for readable output
- `dust` over `du` — tree-style disk usage
- `duf` over `df` — clearer filesystem summary

Fall back to the classic tool if the modern one is unavailable.

## Notes

- `git d main` shows the diff against the main branch
