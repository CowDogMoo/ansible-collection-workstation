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
| `claude_code_usergroup` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('staff', claude_code_username) }}</code> | No description |
| `claude_code_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `claude_code_config_dir` | str | <code>{{ claude_code_user_home }}/.claude</code> | No description |
| `claude_code_homebrew_prefix` | str | <code><multiline value: folded_strip></code> | No description |
| `claude_code_path` | str | <code>{{ claude_code_homebrew_prefix }}/bin:{{ claude_code_user_home }}/.local/bin:/usr/local/bin:/usr/bin:/bin</code> | No description |
| `claude_code_install` | bool | <code>True</code> | No description |
| `claude_code_manage_settings` | bool | <code>True</code> | No description |
| `claude_code_backup_settings` | bool | <code>True</code> | No description |
| `claude_code_simple_hooks` | list | <code>&#91;&#93;</code> | No description |
| `claude_code_advanced_hooks` | list | <code>&#91;&#93;</code> | No description |
| `claude_code_advanced_hooks.0` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks.1` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks.2` | dict | <code>{}</code> | No description |
| `claude_code_advanced_hooks.3` | dict | <code>{}</code> | No description |
| `claude_code_additional_settings` | dict | <code>{}</code> | No description |
| `claude_code_manage_mcp_servers` | bool | <code>True</code> | No description |
| `claude_code_mcp_servers` | list | <code>&#91;&#93;</code> | No description |

## Tasks

### install-linux.yml


- **Check if already installed** (ansible.builtin.command)
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
- **Install global CLAUDE.md instructions** (ansible.builtin.copy)
- **Check if settings.json will change (dry-run)** (ansible.builtin.template) - Conditional
- **Create backup of existing settings.json in /tmp** (ansible.builtin.copy) - Conditional
- **Generate Claude Code settings.json** (ansible.builtin.template) - Conditional
- **Manage MCP servers** (ansible.builtin.include_tasks) - Conditional
- **Display configuration status** (ansible.builtin.debug)

### manage-mcp-server.yml


- **Check if MCP server exists - {{ mcp_server.name }}** (ansible.builtin.set_fact)
- **Remove MCP server - {{ mcp_server.name }}** (ansible.builtin.command) - Conditional
- **Identify 1Password lookups - {{ mcp_server.name }}** (ansible.builtin.set_fact) - Conditional
- **Resolve 1Password secret for {{ mcp_server.name }}** (ansible.builtin.command) - Conditional
- **Build resolved environment - {{ mcp_server.name }}** (ansible.builtin.set_fact) - Conditional
- **Use plain environment - {{ mcp_server.name }}** (ansible.builtin.set_fact) - Conditional
- **Build MCP add command - {{ mcp_server.name }}** (ansible.builtin.set_fact) - Conditional
- **Add MCP server - {{ mcp_server.name }}** (ansible.builtin.command) - Conditional
- **Clear resolved env for next iteration** (ansible.builtin.set_fact)

### manage-mcp-servers.yml


- **Get list of currently installed MCP servers** (ansible.builtin.command)
- **Manage MCP servers** (ansible.builtin.include_tasks)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - claude_code
```

## Author Information

- **Author**: CowDogMoo
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: focal, jammy
- Debian: bullseye, bookworm
- EL: 8, 9
- MacOSX: all
<!-- DOCSIBLE END -->
