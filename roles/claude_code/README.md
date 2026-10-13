<!-- DOCSIBLE START -->
# claude_code

## Description

Manages Claude Code CLI configuration including hooks and settings

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `claude_code_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `claude_code_usergroup` | str | <code>{{ (ansible_facts&#91;'user_gid'&#93; &#124; default('staff')) if ansible_facts&#91;'os_family'&#93; == 'Darwin' else claude_code_username }}</code> | No description |
| `claude_code_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `claude_code_config_dir` | str | <code>{{ claude_code_user_home }}/.claude</code> | No description |
| `claude_code_rules_file` | str | <code>{{ claude_code_config_dir }}/CLAUDE.md</code> | No description |
| `claude_code_rules_src` | str | <code>CLAUDE.md</code> | No description |
| `claude_code_rules_content` | str | <code></code> | No description |
| `claude_code_rules_dir` | str | <code>{{ claude_code_config_dir }}/rules</code> | No description |
| `claude_code_rules_src_dir` | str | <code></code> | No description |
| `claude_code_scripts_dir` | str | <code>{{ claude_code_config_dir }}/scripts</code> | No description |
| `claude_code_scripts_src_dir` | str | <code></code> | No description |
| `claude_code_settings_src` | str | <code></code> | No description |
| `claude_code_homebrew_prefix` | str | <code><multiline value: folded_strip></code> | No description |
| `claude_code_path` | str | <code>{{ claude_code_homebrew_prefix }}/bin:{{ claude_code_user_home }}/.local/bin:/usr/local/bin:/usr/bin:/bin</code> | No description |
| `claude_code_install` | bool | <code>True</code> | No description |
| `claude_code_manage_settings` | bool | <code>True</code> | No description |
| `claude_code_manage_rules` | bool | <code>True</code> | No description |
| `claude_code_manage_scripts` | bool | <code>True</code> | No description |
| `claude_code_backup_settings` | bool | <code>True</code> | No description |
| `claude_code_settings_backup_dir` | str | <code>{{ claude_code_config_dir }}/backups</code> | No description |
| `claude_code_settings_backup_keep` | int | <code>10</code> | No description |
| `claude_code_simple_hooks` | list | <code>&#91;&#93;</code> | No description |
| `claude_code_advanced_hooks_default` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.forbidden_content` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.dangerous_flags` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.post_commit_check` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.post_pr_check` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.stop_sound` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_default.notify_sound` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks_overrides` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks` | str | <code><multiline value: folded_strip></code> | No description |
| `claude_code_attribution` | dict | <code>{}</code> | No description |
| `claude_code_attribution.commit` | str | <code></code> | No description |
| `claude_code_attribution.pr` | str | <code></code> | No description |
| `claude_code_attribution.sessionUrl` | bool | <code>False</code> | No description |
| `claude_code_skip_dangerous_mode_permission_prompt` | bool | <code>False</code> | No description |
| `claude_code_additional_settings` | dict | <code>{}</code> | No description |
| `claude_code_manage_mcp_servers` | bool | <code>True</code> | No description |
| `claude_code_mcp_servers` | list | <code>&#91;&#93;</code> | No description |
| `claude_code_manage_remote_control` | bool | <code>True</code> | On macOS, run claude remote-control hosts as LaunchAgents for the directories in the hosts file. |
| `claude_code_remote_control_config` | str | <code>{{ claude_code_user_home }}/.config/claude-rc/hosts.yml</code> | Private YAML hosts file read on the target; the role never writes it, and skips this step when it is absent. |
| `claude_code_remote_control_spawn` | str | <code>worktree</code> | Spawn mode for hosts that don't set spawn; worktree needs a git repository. |
| `claude_code_remote_control_capacity` | int | <code>32</code> | Max concurrent sessions for hosts that don't set capacity. |
| `claude_code_remote_control_permission_mode` | str | <code></code> | Permission mode for spawned sessions when a host doesn't set permission_mode; empty leaves Claude Code's default. |
| `claude_code_remote_control_chrome` | bool | <code>True</code> | Give spawned sessions Claude in Chrome when a host doesn't set chrome. |
| `claude_code_remote_control_label_prefix` | str | <code>com.cowdogmoo.claude-rc</code> | LaunchAgent label prefix; agents under it that the hosts file doesn't list are removed. |
| `claude_code_remote_control_throttle_interval` | int | <code>30</code> | Seconds launchd waits before restarting a host that exited. |
| `claude_code_remote_control_log_dir` | str | <code>{{ claude_code_user_home }}/logs/claude-remote-control</code> | Directory for each host's combined stdout and stderr log, <name>.log. |
| `claude_code_remote_control_binary` | str | <code></code> | Path to the claude binary; empty uses the first existing binary candidate. |
| `claude_code_remote_control_binary_candidates` | list | <code>&#91;&#93;</code> | Paths tried in order when claude_code_remote_control_binary is empty. |
| `claude_code_remote_control_binary_candidates.0` | str | <code>{{ claude_code_user_home }}/.local/bin/claude</code> | No description |
| `claude_code_remote_control_binary_candidates.1` | str | <code>{{ claude_code_homebrew_prefix }}/bin/claude</code> | No description |
| `claude_code_remote_control_path` | str | <code><multiline value: folded_strip></code> | PATH given to each host, since launchd starts agents without a shell profile. |
| `claude_code_remote_control_base_environment` | dict | <code>{}</code> | Environment for each host (HOME, USER, LOGNAME, SHELL, PATH, LANG). |
| `claude_code_remote_control_base_environment.HOME` | str | <code>{{ claude_code_user_home }}</code> | No description |
| `claude_code_remote_control_base_environment.USER` | str | <code>{{ claude_code_username }}</code> | No description |
| `claude_code_remote_control_base_environment.LOGNAME` | str | <code>{{ claude_code_username }}</code> | No description |
| `claude_code_remote_control_base_environment.SHELL` | str | <code>{{ ansible_facts&#91;'user_shell'&#93; &#124; default('/bin/zsh') }}</code> | No description |
| `claude_code_remote_control_base_environment.PATH` | str | <code>{{ claude_code_remote_control_path &#124; trim }}</code> | No description |
| `claude_code_remote_control_base_environment.LANG` | str | <code>en_US.UTF-8</code> | No description |
| `claude_code_remote_control_environment` | dict | <code>{}</code> | Extra environment variables for every host, merged over the base environment. |

## Tasks

### backup-settings.yml


- **Check for an existing settings.json** (ansible.builtin.stat)
- **Back up and prune settings.json copies** (block) - Conditional
- **Create settings.json backup directory** (ansible.builtin.file)
- **Copy existing settings.json into the backup directory** (ansible.builtin.copy)
- **Find settings.json backups** (ansible.builtin.find)
- **Prune settings.json backups beyond the retention limit** (ansible.builtin.file) - Conditional

### install-linux.yml


- **Check if already installed** (ansible.builtin.command)
- **Check for user-local install** (ansible.builtin.stat)
- **Check if npm is available** (ansible.builtin.command) - Conditional
- **Install via npm** (community.general.npm) - Conditional
- **Install via script (fallback)** (ansible.builtin.shell) - Conditional
- **Verify installation** (ansible.builtin.command)
- **Display version** (ansible.builtin.debug) - Conditional

### install-macos.yml


- **Check if already installed** (ansible.builtin.command)
- **Install via Homebrew** (community.general.homebrew_cask) - Conditional
- **Verify installation** (ansible.builtin.command)
- **Display version** (ansible.builtin.debug) - Conditional

### install-windows.yml


- **Check if already installed** (ansible.windows.win_command)
- **Check if npm is available** (ansible.windows.win_command) - Conditional
- **Install via npm** (ansible.windows.win_shell) - Conditional
- **Install via PowerShell (fallback)** (ansible.windows.win_shell) - Conditional
- **Verify installation** (ansible.windows.win_command)
- **Display version** (ansible.builtin.debug) - Conditional

### main.yml


- **Set claude_code username for Kali systems** (ansible.builtin.set_fact) - Conditional
- **Ensure claude_code user home directory exists** (ansible.builtin.stat)
- **Fail if user home directory doesn't exist** (ansible.builtin.fail) - Conditional
- **Install Claude Code on macOS** (ansible.builtin.include_tasks) - Conditional
- **Install Claude Code on Linux** (ansible.builtin.include_tasks) - Conditional
- **Install Claude Code on Windows** (ansible.builtin.include_tasks) - Conditional
- **Create Claude Code configuration directory** (ansible.builtin.file)
- **Install global CLAUDE.md instructions** (ansible.builtin.copy) - Conditional
- **Create Claude Code rules directory** (ansible.builtin.file) - Conditional
- **Install Claude Code rules** (ansible.builtin.copy) - Conditional
- **Create Claude Code scripts directory** (ansible.builtin.file) - Conditional
- **Install Claude Code scripts** (ansible.builtin.copy) - Conditional
- **Check if custom settings.json from source will change (dry-run)** (ansible.builtin.copy) - Conditional
- **Check if settings.json will change (dry-run)** (ansible.builtin.template) - Conditional
- **Back up existing settings.json before it is rewritten** (ansible.builtin.include_tasks) - Conditional
- **Install custom Claude Code settings.json from source** (ansible.builtin.copy) - Conditional
- **Generate Claude Code settings.json** (ansible.builtin.template) - Conditional
- **Manage MCP servers** (ansible.builtin.include_tasks) - Conditional
- **Manage Remote Control LaunchAgents on macOS** (ansible.builtin.include_tasks) - Conditional
- **Display configuration status** (ansible.builtin.debug)

### manage-mcp-server.yml


- **Check if MCP server exists - {{ mcp_server.name }}** (ansible.builtin.set_fact)
- **Remove MCP server - {{ mcp_server.name }}** (ansible.builtin.command) - Conditional
- **Build MCP add command - {{ mcp_server.name }}** (ansible.builtin.set_fact) - Conditional
- **Add MCP server - {{ mcp_server.name }}** (ansible.builtin.command) - Conditional

### manage-mcp-servers.yml


- **Get list of currently installed MCP servers** (ansible.builtin.command)
- **Determine whether 1Password resolution is needed** (ansible.builtin.set_fact)
- **Check for the 1Password CLI** (ansible.builtin.command) - Conditional
- **Fail with guidance when op:// references cannot be resolved** (ansible.builtin.fail) - Conditional
- **Create a staging file for 1Password resolution** (ansible.builtin.tempfile) - Conditional
- **Write MCP server definitions for resolution** (ansible.builtin.template) - Conditional
- **Resolve 1Password references** (ansible.builtin.command) - Conditional
- **Remove the staging file** (ansible.builtin.file) - Conditional
- **Verify the resolved definitions still parse** (ansible.builtin.assert) - Conditional
- **Use the resolved MCP server definitions** (ansible.builtin.set_fact)
- **Manage MCP servers** (ansible.builtin.include_tasks)

### remote-control-macos.yml


- **Check for the Remote Control hosts file** (ansible.builtin.stat)
- **Skip Remote Control hosts when there is no hosts file** (ansible.builtin.debug) - Conditional
- **Manage Remote Control LaunchAgents from the hosts file** (block) - Conditional
- **Read the Remote Control hosts file** (ansible.builtin.slurp)
- **Parse the Remote Control hosts file** (ansible.builtin.set_fact)
- **Validate the Remote Control hosts list** (ansible.builtin.assert)
- **Validate Remote Control host entries** (ansible.builtin.assert)
- **Locate the claude binary for Remote Control hosts** (ansible.builtin.stat) - Conditional
- **Pick the first claude binary that exists** (ansible.builtin.set_fact) - Conditional
- **Fail when no claude binary was found** (ansible.builtin.fail) - Conditional
- **Check Remote Control host directories** (ansible.builtin.stat)
- **Fail when a Remote Control host directory is missing** (ansible.builtin.fail) - Conditional
- **Check worktree-mode hosts are in a git repository** (ansible.builtin.command) - Conditional
- **Fail when a worktree-mode host is not in a git repository** (ansible.builtin.fail) - Conditional
- **Create Remote Control log and LaunchAgents directories** (ansible.builtin.file) - Conditional
- **Render Remote Control LaunchAgents** (ansible.builtin.template)
- **Check which Remote Control LaunchAgents are loaded** (ansible.builtin.command)
- **Unload Remote Control LaunchAgents whose plist changed** (ansible.builtin.command) - Conditional
- **Load Remote Control LaunchAgents that changed or are not loaded** (ansible.builtin.command) - Conditional
- **Find Remote Control LaunchAgents under the label prefix** (ansible.builtin.find)
- **Note Remote Control LaunchAgents the hosts file no longer lists** (ansible.builtin.set_fact)
- **Unload Remote Control LaunchAgents the hosts file no longer lists** (ansible.builtin.command)
- **Remove Remote Control LaunchAgents the hosts file no longer lists** (ansible.builtin.file)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - claude_code
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: focal, jammy
- Debian: bullseye, bookworm
- EL: 8, 9
- MacOSX: all
<!-- DOCSIBLE END -->
