# Global Claude Code Instructions

## .claude Directory and Version Control

A project's `.claude/` directory mixes team-shared configuration with personal
state. Commit the shared parts; keep the personal parts out of git.

**Commit these** (team-shared configuration):

- `.claude/settings.json` — shared permissions, hooks, and MCP configuration
- `.claude/agents/` — project subagents
- `.claude/skills/` — project skills
- `.claude/commands/` — project slash commands
- `.claude/rules/` — topic-scoped instruction files
- `CLAUDE.md` (repo root or `.claude/CLAUDE.md`) — project instructions

**NEVER commit these** (personal/local state):

- `.claude/settings.local.json` — personal overrides (Claude Code auto-adds it
  to the global git excludes)
- `.claude/worktrees/`, `.claude/agent-memory-local/`, and any other
  session/cache state
- The global `~/.claude/` directory — it belongs to the user, never to a repo

If a local-only file shows up staged, run `git restore --staged <path>` and add
it to `.gitignore` — but never blanket-ignore the whole `.claude/` directory,
since that hides shared agents, skills, and settings from the team.

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

## Browser Automation (Claude in Chrome)

Use the built-in Chrome integration (`claude --chrome`, or `/chrome` → "Enabled by
default"). It opens new tabs in the **already-running** Chrome and shares its login
state, so sites you're signed into stay signed in.

**Do NOT add `chrome-devtools-mcp`, `@playwright/mcp`, or `puppeteer` as MCP servers
for general browsing.** They launch a separate browser on their own throwaway
profile (`~/.cache/chrome-devtools-mcp/`, `~/.cache/ms-playwright/`), which means
re-authenticating everywhere. Reach for them only when you specifically need
headless/CI browsing, and remove them afterward (`claude mcp remove <name> --scope user`).

Requires OAuth login. API-key auth, or Bedrock/Vertex/Foundry, disables the Chrome
integration entirely.

### Session startup

ALWAYS call `tabs_context_mcp` first, before any other browser tool.

Tab IDs are per-session and go stale. Never reuse an ID from earlier in the
conversation or from a previous session.

- Only work in an existing tab if explicitly asked; otherwise `tabs_create_mcp`.
- On any "tab doesn't exist" / invalid-tab error, re-call `tabs_context_mcp` for
  fresh IDs instead of retrying the same ID. Same after a closed tab or failed
  navigation.

### Reading pages

Prefer, in order: `find` (locating an element or string) → `get_page_text` (content
as text) → `read_page` (interactive element map, for clicking and typing) →
screenshot (only when layout or visual state actually matters).

Never screenshot just to read text — it costs far more and reads worse.

### Modal dialogs

**NEVER trigger `alert()`, `confirm()`, `prompt()`, or native browser modals.** They
block the extension's event loop and every subsequent tool call hangs until a human
dismisses the dialog by hand.

- Avoid clicking elements likely to confirm-prompt (Delete, Discard, Leave site).
  If unavoidable, warn first that the session may stall.
- Debug with `console.log` via `javascript_tool` + `read_console_messages`, never
  `alert()`.
- If one fires and tools stop responding, stop and say so. Do not keep retrying.

### Debugging

`read_console_messages` and `read_network_requests` are verbose. Always pass the
`pattern` regex to filter (`"\\[MyApp\\]"`, `"error|failed"`) instead of dumping
everything.

### Don't spiral

Stop and ask for direction when the same call fails 2–3 times, the extension stops
responding, elements ignore clicks, pages won't load, or the task pulls into
unrelated pages. Say what you tried and what went wrong. Never re-run a failing
action indefinitely.

### Misc

- Batch independent actions into one `browser_batch` call.
- For multi-step flows worth reviewing, record with `gif_creator` — capture a few
  extra frames before the first and after the last action, and name the file for
  what it shows (`login_flow.gif`, not `output.gif`).

## Notes

- `git d main` shows the diff against the main branch
