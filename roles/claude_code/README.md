<!-- DOCSIBLE START -->
# claude_code

## Description

Manages Claude Code CLI configuration including hooks and settings

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `claude_code_username` | str | `{{ ansible_user_id | default(ansible_user) }}` | No description |
| `claude_code_usergroup` | str | `{{ (ansible_facts['os_family'] == 'Darwin') | ternary('staff', claude_code_username) }}` | No description |
| `claude_code_user_home` | str | `<multiline value: folded_strip>` | No description |
| `claude_code_config_dir` | str | `{{ claude_code_user_home }}/.claude` | No description |
| `claude_code_install` | bool | `True` | No description |
| `claude_code_manage_settings` | bool | `True` | No description |
| `claude_code_backup_settings` | bool | `True` | No description |
| `claude_code_simple_hooks` | list | `[]` | No description |
| `claude_code_advanced_hooks` | list | `[]` | No description |
| `claude_code_advanced_hooks.0` | dict | `{}` | No description |
| `claude_code_additional_settings` | dict | `{}` | No description |

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
- **Generate Claude Code settings.json** (ansible.builtin.template) - Conditional
- **Display configuration status** (ansible.builtin.debug)

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
