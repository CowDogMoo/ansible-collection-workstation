# Ansible Role: claude_code

Installs and manages Claude Code CLI, including installation, configuration, hooks, and settings.

## Description

This role installs Claude Code CLI and manages the configuration file (`~/.claude/settings.json`). Installation methods are platform-specific:

- **macOS**: Homebrew
- **Linux**: npm (if available) or install script
- **Windows**: npm (if available) or PowerShell script

Claude Code hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle.

## Requirements

- Ansible 2.15 or higher
- For macOS: Homebrew installed
- For Linux/Windows with npm method: Node.js 18+ and npm installed
- Internet connection for downloading Claude Code CLI

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# User configuration
claude_code_username: "{{ ansible_user_id | default(ansible_user) }}"
claude_code_usergroup: "{{ (ansible_facts['os_family'] == 'Darwin') | ternary('staff', claude_code_username) }}"
claude_code_user_home: "{{ ... }}"

# Configuration directory for Claude Code
claude_code_config_dir: "{{ claude_code_user_home }}/.claude"

# Whether to install Claude Code CLI
claude_code_install: true

# Whether to manage Claude Code settings
claude_code_manage_settings: true

# Whether to backup existing settings before overwriting
claude_code_backup_settings: true

# Simple hooks - easy to configure, no coding required
claude_code_simple_hooks:
  - name: "Hook test notification"
    action: notify
    message: "🔔 Hooks working!"

  - name: "Require fabric for git commits"
    command_pattern: 'git\s+commit.*-m'
    exclude_pattern: 'fabric'
    action: block
    message: "Use fabric for commit messages"

  - name: "Require fabric for PRs"
    command_contains: 'gh pr create'
    action: block
    message: "Use fabric for PR descriptions"

# Advanced hooks - for custom Python/shell scripts
claude_code_advanced_hooks: []

# Additional Claude Code settings
claude_code_additional_settings: {}
```

### Hook Configuration

**📖 [Complete Documentation](docs/HOOKS_GUIDE.md)** | **[Examples](files/hook_examples.yml)** | **[Python Helpers](files/hook_helpers.py)**

**Simple Hooks** - No coding required:

- `action`: `notify` or `block`
- `message`: Message to display
- `command_pattern`: Regex (optional)
- `command_contains`: String match (optional)
- `exclude_pattern`: Exclusion filter (optional)

**Advanced Hooks** - Custom Python/shell scripts for complex logic

## Dependencies

None.

## Example Playbook

### Basic usage (default hooks)

```yaml
- hosts: localhost
  roles:
    - cowdogmoo.workstation.claude_code
```

### Custom hooks

```yaml
- hosts: localhost
  roles:
    - cowdogmoo.workstation.claude_code
      vars:
        claude_code_simple_hooks:
          - name: "Block dangerous rm"
            command_contains: "rm -rf /"
            action: block
            message: "Dangerous command blocked!"

          - name: "Require code review"
            command_pattern: 'git\s+push.*main'
            action: block
            message: "Direct push to main not allowed"
```

### Disable default hooks

```yaml
- hosts: localhost
  roles:
    - cowdogmoo.workstation.claude_code
      vars:
        claude_code_simple_hooks: []
        claude_code_advanced_hooks: []
```

## Features

- **Fabric Integration**: Default hooks enforce using Fabric for git commits and PR descriptions
- **Automatic Backups**: Settings are backed up when changed (timestamps preserved)
- **Idempotent**: Safe to run multiple times without side effects
- **Multi-platform**: Works on macOS, Linux, and Windows

## License

MIT

## Author Information

This role was created by CowDogMoo.

## References

- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks-guide)
- [Claude Code Configuration Guide](https://www.eesel.ai/blog/settings-json-claude-code)
- [Fabric AI Framework](https://github.com/danielmiessler/fabric)
