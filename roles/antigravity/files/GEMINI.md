# Global Antigravity Instructions

## .gemini Directory and Version Control

Project-level agent configuration is team-shared and belongs in git; personal
state and credentials never do.

**Commit these** (team-shared configuration):

- `.gemini/settings.json` — project-scoped Gemini CLI settings (use `$VAR_NAME`
  env-var syntax so secrets stay out of the file)
- `.gemini/commands/` — project custom commands
- `.agent/rules/` and `.agent/workflows/` — Antigravity workspace rules and
  workflows
- `GEMINI.md` / `AGENTS.md` at the repo root — project context and rules

**NEVER commit these** (personal/local state and credentials):

- The global `~/.gemini/` directory — it holds OAuth credentials
  (`oauth_creds.json`, `google_accounts.json`) and belongs to the user, never
  to a repo
- `.env` files or anything else containing API keys
- Session/cache state such as `.gemini/tmp/`

If a local-only file shows up staged, run `git restore --staged <path>` and add
it to `.gitignore` — but never blanket-ignore the whole `.gemini/` or `.agent/`
directory, since that hides shared settings, commands, rules, and workflows
from the team.

## Git Workflow

### Commits

Always use `squad_commit` for commit messages (billed to the Claude
subscription via squad's claude-code provider). If it fails, fall back to
`fabric_commit` (API-billed):

```bash
squad_commit
```

**NEVER EVER use --no-verify when committing or there will be dire consequences!**

- Never skip pre-commit hooks with `--no-verify` or `-n`
- Hooks are there for critical validation and security checks
- If a commit fails due to hooks, fix the issue and create a NEW commit
- Bypassing hooks can lead to broken builds, security vulnerabilities, and other serious problems

### Pull Requests

Always use `squad_pr` for pull requests — both to **open** them and to **update** them (billed to the Claude subscription; fall back to `fabric_pr` if it fails). `squad_pr` regenerates the title/body from the current `git diff main`, then creates the PR or, if one already exists for the branch, updates that PR in place.

```bash
squad_pr
```

**The PR title and body must ALWAYS be `squad_pr`'s generated output. NEVER hand-write or hand-edit them.**

- Any time the branch changes — after a **rebase, amend, new commits, or force-push** — the existing body is stale. Re-run `squad_pr`; it regenerates from the new diff and updates the existing PR. This is the ONLY correct way to refresh a PR body.
- Do **not** run `gh pr edit --body "..."` (or `--title`) with text you wrote yourself, and do not "clean up", "correct", or "just fix" the body by hand. Substituting your own writing for the generated output breaks this rule no matter how small the change. If the body needs to change, re-run `squad_pr`.

**Format verification — after every `squad_pr`:**

1. Check the PR with `gh pr view`.
2. Confirm the generated output is clean: **no code fences (```)** in the title or body, and the **title is not duplicated** in the body.
3. If the output is malformed, the bug is in the `pr` pattern or the filter — both live in `~/cowdogmoo/fabric-patterns-hub` (`patterns/pr/system.md`, `scripts/filter.py`) — fix it at the source and re-run `squad_pr`. Never patch the symptom by hand-editing the PR.

Both `squad_pr` and `fabric_pr` share the same patterns and filters from `~/cowdogmoo/fabric-patterns-hub`, so a source fix applies to both.

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
