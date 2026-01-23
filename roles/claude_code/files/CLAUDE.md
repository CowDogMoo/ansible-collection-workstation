# Global Claude Code Instructions

## CRITICAL: .claude Directory

**NEVER EVER commit the .claude directory or any of its contents to git!**

- The `.claude/` directory and its contents are personal/local configuration
- Always ensure `.claude/` is in `.gitignore`
- Never add, stage, or commit any files from `.claude/`
- If `.claude/` appears in git status as staged, immediately run `git restore --staged .claude/`

## Git Workflow

### Commits

Always use fabric for commit messages:

```bash
git ds | fabric --pattern commit | git commit -F -
```

**IMPORTANT**: Always remove code fences (```) from commit messages before committing. If a generated commit message contains code fences, strip them out completely.

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

## Notes

- `git ds` is an alias for `git diff --staged` (shows staged changes)
- `git d main` shows the diff against the main branch
- The fabric patterns will generate properly formatted commit messages and PR descriptions
- Use `-F -` to read from stdin
