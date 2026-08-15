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

Always use the `fabric_pr` function to create pull requests:

```bash
fabric_pr
```

**CRITICAL POST-CREATION VERIFICATION**:

After `fabric_pr` creates the PR, you MUST verify and fix if needed:

1. **Check the created PR** using `gh pr view` to see the title and body
2. **Verify requirements**:
   - **No code fences (```)** in the title or body
   - **No duplicate title** - the title text must NOT appear in the body
3. **If violations found**, update the PR immediately using `gh pr edit`:

   ```bash
   gh pr edit --body "corrected body without code fences or duplicate title"
   ```

The `fabric_pr` function should handle these automatically, but you must verify and correct any issues in the created PR.

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
