# Remote Control hosts as LaunchAgents (macOS)

`claude remote-control` (`claude rc`) keeps a host running in a directory so
sessions can be started and driven from claude.ai/code or the Claude mobile
app. Run by hand, every host needs a terminal tab left open. On macOS this role
can run each host as a LaunchAgent instead: it starts at login, restarts if it
exits, and needs no terminal.

Which directories get a host is private to each machine, so the list lives in
a file outside this repository, `~/.config/claude-rc/hosts.yml` by default
(`claude_code_remote_control_config`). The role reads it on the target and
never writes it.

## The hosts file

```yaml
hosts:
  - name: example # required; LaunchAgent label suffix and log name
    dir: ~/src/example # required; ~ expands to your home directory
    permission_mode: bypassPermissions
  - name: notes
    dir: ~/src/notes
    spawn: same-dir # this directory is not a git repository
    capacity: 8
```

| Key               | Required | Default                                         | Meaning                                                          |
| ----------------- | -------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| `name`            | yes      |                                                 | Unique; letters, digits, `_`, `.`, `-`                           |
| `dir`             | yes      |                                                 | Existing directory the host serves                               |
| `spawn`           | no       | `worktree` (`claude_code_remote_control_spawn`) | `same-dir`, `worktree` (needs a git repository), or `session`    |
| `capacity`        | no       | `32` (`claude_code_remote_control_capacity`)    | Max concurrent sessions; ignored for `session`                   |
| `permission_mode` | no       | Claude Code's own default                       | Permission mode for spawned sessions, e.g. `bypassPermissions`   |
| `chrome`          | no       | `true` (`claude_code_remote_control_chrome`)    | Claude in Chrome for spawned sessions (`--chrome`/`--no-chrome`) |

Each host becomes `~/Library/LaunchAgents/com.cowdogmoo.claude-rc.<name>.plist`
running:

```text
claude remote-control --spawn <spawn> --capacity <capacity> [--permission-mode <mode>] --chrome
```

with `RunAtLoad`, `KeepAlive`, a 30 second `ThrottleInterval`, and
`LimitLoadToSessionType` `Aqua` (only in the logged-in desktop session, where
the login keychain and Chrome are). stdout and stderr go to
`~/logs/claude-remote-control/<name>.log`, which the workstation playbook
rotates with copytruncate.

The file is the source of truth:

- A host whose plist changed is reloaded; one that is unchanged and running is
  left alone, so a converge does not drop live sessions.
- A host removed from the file is unloaded and its plist deleted on the next
  run. `hosts: []` removes them all.
- With no file at all the role skips this step and leaves any existing agents
  in place.

## Before a directory can run headless

- **Trust the directory once.** Claude Code asks whether to trust a folder the
  first time it runs there, and launchd has no terminal to answer on. An
  untrusted directory logs `Workspace not trusted` and launchd retries it every
  30 seconds. Run `claude` in the directory once and accept the prompt. Trust
  is recorded per directory; a trusted parent does not cover its children.
- **Your home folder may need a terminal tab.** If Claude Code does not
  persist trust for your home folder, a host there can't start under launchd.
  Keep that one in a terminal tab instead of the hosts file.
- **Worktree mode needs git.** The role fails a host with `spawn: worktree`
  outside a git repository. Use `same-dir` there.
- **One host per directory.** A LaunchAgent host exits with `This folder is
  already served by a terminal claude remote-control` while a terminal host
  serves the same directory, and keeps retrying until it is stopped.

## Switching over from terminal tabs

1. Create `~/.config/claude-rc/hosts.yml` listing this machine's directories.
   It stays on this machine; don't commit it. Tabs started with
   `claude rc --permission-mode bypassPermissions` need
   `permission_mode: bypassPermissions` on every entry: without it, spawned
   sessions fall back to Claude Code's default mode and ask before each tool.
2. Close the iTerm2 tabs running `claude rc` for those directories. Closing a
   tab stops that host, and every session it is serving drops with it, so
   finish or hand off anything in progress first. Start new sessions from
   claude.ai/code once the agents are up.
3. Run the workstation playbook with the `claude` tag:

   ```bash
   ansible-playbook playbooks/workstation/workstation.yml --tags claude
   ```

   The `claude` tag only touches this role; the next full run also installs
   the log rotation config for `~/logs/claude-remote-control`.

4. Check each host: `launchctl print gui/$(id -u)/com.cowdogmoo.claude-rc.<name>`
   should show `state = running`, and `~/logs/claude-remote-control/<name>.log`
   should show `Connected`.

To stop one host for a while, `launchctl bootout gui/$(id -u)/com.cowdogmoo.claude-rc.<name>`;
the next playbook run loads it again. To remove it for good, delete its entry
from the hosts file and rerun the playbook.
