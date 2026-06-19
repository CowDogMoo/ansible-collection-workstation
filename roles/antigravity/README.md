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
| `antigravity_usergroup` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('staff', antigravity_username) }}</code> | No description |
| `antigravity_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `antigravity_config_dir` | str | <code>{{ antigravity_user_home }}/.gemini/config</code> | No description |
| `antigravity_homebrew_prefix` | str | <code><multiline value: folded_strip></code> | No description |
| `antigravity_path` | str | <code>{{ antigravity_homebrew_prefix }}/bin:{{ antigravity_user_home }}/.local/bin:/usr/local/bin:/usr/bin:/bin</code> | No description |
| `antigravity_install` | bool | <code>True</code> | No description |
| `antigravity_manage_settings` | bool | <code>True</code> | No description |
| `antigravity_manage_plugins` | bool | <code>True</code> | No description |
| `antigravity_plugins` | list | <code>&#91;&#93;</code> | No description |

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
- **Create Antigravity configuration directory** (ansible.builtin.file)
- **Install global AGENTS.md instructions** (ansible.builtin.copy) - Conditional
- **Manage plugins** (ansible.builtin.include_tasks) - Conditional
- **Display configuration status** (ansible.builtin.debug)

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
