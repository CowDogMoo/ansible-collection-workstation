<!-- DOCSIBLE START -->
# antigravity

## Description

Manages Antigravity CLI configuration including hooks and settings

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `antigravity_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `antigravity_usergroup` | str | <code>{{ (ansible_facts&#91;'user_gid'&#93; &#124; default('staff')) if ansible_facts&#91;'os_family'&#93; == 'Darwin' else antigravity_username }}</code> | No description |
| `antigravity_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `antigravity_config_dir` | str | <code>{{ antigravity_user_home }}/.gemini/config</code> | No description |
| `antigravity_rules_file` | str | <code>{{ antigravity_user_home }}/.gemini/GEMINI.md</code> | No description |
| `antigravity_rules_src` | str | <code>GEMINI.md</code> | No description |
| `antigravity_rules_content` | str | <code></code> | No description |
| `antigravity_rules_dir` | str | <code>{{ antigravity_config_dir }}/rules</code> | No description |
| `antigravity_rules_src_dir` | str | <code></code> | No description |
| `antigravity_hooks_file` | str | <code>{{ antigravity_config_dir }}/hooks.json</code> | No description |
| `antigravity_mcp_config_file` | str | <code>{{ antigravity_config_dir }}/mcp_config.json</code> | No description |
| `antigravity_homebrew_prefix` | str | <code><multiline value: folded_strip></code> | No description |
| `antigravity_path` | str | <code>{{ antigravity_homebrew_prefix }}/bin:{{ antigravity_user_home }}/.local/bin:/usr/local/bin:/usr/bin:/bin</code> | No description |
| `antigravity_install` | bool | <code>True</code> | No description |
| `antigravity_manage_settings` | bool | <code>True</code> | No description |
| `antigravity_manage_rules` | bool | <code>True</code> | No description |
| `antigravity_manage_hooks` | bool | <code>True</code> | No description |
| `antigravity_backup_settings` | bool | <code>True</code> | No description |
| `antigravity_manage_plugins` | bool | <code>True</code> | No description |
| `antigravity_plugins` | list | <code>&#91;&#93;</code> | No description |
| `antigravity_hooks_default` | dict | <code>{}</code> | No description |
| `antigravity_hooks_default.forbidden_content` | dict | <code>{}</code> | No description |
| `antigravity_hooks_default.dangerous_flags` | dict | <code>{}</code> | No description |
| `antigravity_hooks_default.post_commit_check` | dict | <code>{}</code> | No description |
| `antigravity_hooks_default.stop_sound` | dict | <code>{}</code> | No description |
| `antigravity_hooks_overrides` | dict | <code>{}</code> | No description |
| `antigravity_hooks` | str | <code><multiline value: folded_strip></code> | No description |
| `antigravity_manage_mcp_servers` | bool | <code>True</code> | No description |
| `antigravity_mcp_op_required` | bool | <code>False</code> | No description |
| `antigravity_mcp_servers` | list | <code>&#91;&#93;</code> | No description |

## Tasks

### install-linux.yml


- **Check if already installed** (ansible.builtin.command)
- **Install via Homebrew** (community.general.homebrew) - Conditional
- **Print manual install notice** (ansible.builtin.debug) - Conditional
- **Verify installation** (ansible.builtin.command)
- **Display version** (ansible.builtin.debug) - Conditional

### install-macos.yml


- **Check if already installed** (ansible.builtin.command)
- **Install via Homebrew** (community.general.homebrew) - Conditional
- **Verify installation** (ansible.builtin.command)
- **Display version** (ansible.builtin.debug) - Conditional

### install-windows.yml


- **Check if already installed** (ansible.builtin.command)
- **Print manual install notice** (ansible.builtin.debug) - Conditional
- **Verify installation** (ansible.builtin.command)
- **Display version** (ansible.builtin.debug) - Conditional

### main.yml


- **Set antigravity username for Kali systems** (ansible.builtin.set_fact) - Conditional
- **Ensure antigravity user home directory exists** (ansible.builtin.stat)
- **Fail if user home directory doesn't exist** (ansible.builtin.fail) - Conditional
- **Install Antigravity on macOS** (ansible.builtin.include_tasks) - Conditional
- **Install Antigravity on Linux** (ansible.builtin.include_tasks) - Conditional
- **Install Antigravity on Windows** (ansible.builtin.include_tasks) - Conditional
- **Create Antigravity home directory** (ansible.builtin.file)
- **Create Antigravity configuration directory** (ansible.builtin.file)
- **Install global GEMINI.md instructions** (ansible.builtin.copy) - Conditional
- **Create Antigravity rules directory** (ansible.builtin.file) - Conditional
- **Install Antigravity rules** (ansible.builtin.copy) - Conditional
- **Check if hooks.json will change (dry-run)** (ansible.builtin.template) - Conditional
- **Create backup of existing hooks.json in /tmp** (ansible.builtin.copy) - Conditional
- **Generate Antigravity hooks.json** (ansible.builtin.template) - Conditional
- **Manage MCP servers** (ansible.builtin.include_tasks) - Conditional
- **Manage plugins** (ansible.builtin.include_tasks) - Conditional
- **Display configuration status** (ansible.builtin.debug)

### manage-mcp-servers.yml


- **Check for existing MCP configuration** (ansible.builtin.stat)
- **Read existing MCP configuration** (ansible.builtin.slurp) - Conditional
- **Parse existing MCP servers** (block)
- **Extract mcpServers from the existing configuration** (ansible.builtin.set_fact)
- **Determine whether 1Password resolution is needed** (ansible.builtin.set_fact)
- **Check for the 1Password CLI** (ansible.builtin.command) - Conditional
- **Fail with guidance when op:// references are required but unresolvable** (ansible.builtin.fail) - Conditional
- **Warn that servers carrying op:// references are being skipped** (ansible.builtin.debug) - Conditional
- **Skip the servers whose op:// references cannot be resolved** (ansible.builtin.set_fact) - Conditional
- **Resolve 1Password references in MCP configuration** (block) - Conditional
- **Create a staging file for 1Password resolution** (ansible.builtin.tempfile)
- **Write MCP configuration for resolution** (ansible.builtin.template)
- **Resolve 1Password references** (ansible.builtin.command)
- **Remove the staging file** (ansible.builtin.file)
- **Verify the resolved configuration still parses** (ansible.builtin.assert)
- **Write MCP configuration** (ansible.builtin.template) - Conditional
- **Write MCP configuration with resolved 1Password references** (ansible.builtin.copy) - Conditional

### manage-plugin.yml


- **Check if plugin exists - {{ plugin.name }}** (ansible.builtin.set_fact)
- **Remove plugin - {{ plugin.name }}** (ansible.builtin.command) - Conditional
- **Add plugin - {{ plugin.name }}** (ansible.builtin.command) - Conditional

### manage-plugins.yml


- **Get list of currently installed plugins** (ansible.builtin.command)
- **Manage plugins** (ansible.builtin.include_tasks)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - antigravity
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
