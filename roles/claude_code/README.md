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
claude_code_config_dir: "{{ claude_code_user_home }}/.config/claude"

# Whether to install Claude Code CLI
claude_code_install: true

# Whether to manage Claude Code settings
claude_code_manage_settings: true

# Whether to backup existing settings before overwriting
claude_code_backup_settings: true

# Claude Code hooks configuration
claude_code_hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "python3 -c \"import sys; sys.stderr.write('🔔 HOOK TEST: Hooks system is working!\\n'); sys.exit(0)\""
        - type: "command"
          command: "python3 -c \"import json, sys, re; data=json.load(sys.stdin); cmd=data.get('tool_input',{}).get('command',''); is_git_commit=bool(re.search(r'git\\\\s+commit.*-m', cmd)) and 'fabric' not in cmd; msg='❌ BLOCKED: Do not use git commit -m directly.\\\\n\\\\n✅ Use fabric for commit messages:\\\\n   git diff --staged | fabric --pattern commit\\\\n\\\\nThen commit with:\\\\n   git commit -m \\\\\"$(git diff --staged | fabric --pattern commit)\\\\\"' if is_git_commit else ''; sys.stderr.write(msg + '\\\\n') if msg else None; sys.exit(2 if msg else 0)\""
        - type: "command"
          command: "python3 -c \"import json, sys; data=json.load(sys.stdin); cmd=data.get('tool_input',{}).get('command',''); is_pr_create='gh pr create' in cmd; msg='❌ BLOCKED: Generate PR description first.\\\\n\\\\n✅ Use fabric for PR descriptions:\\\\n   git diff main...HEAD | fabric --pattern commit' if is_pr_create else ''; sys.stderr.write(msg + '\\\\n') if msg else None; sys.exit(2 if msg else 0)\""

# Additional Claude Code settings
claude_code_additional_settings: {}
```

## Hook Events

Claude Code supports multiple hook events:

- `UserPromptSubmit` - When user submits a prompt before Claude processes it
- `PreToolUse` - Before any tool execution (can block tool execution)
- `PostToolUse` - After successful tool completion

## Dependencies

None.

## Example Playbook

### Basic usage with default hooks

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.claude_code
```

### Custom hooks configuration

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.claude_code
      vars:
        claude_code_hooks:
          PreToolUse:
            - matcher: "Bash"
              hooks:
                - type: "command"
                  command: "python3 -c \"import json, sys; data=json.load(sys.stdin); cmd=data.get('tool_input',{}).get('command',''); is_lint='git commit' in cmd; msg='⚠️  Run linters before committing' if is_lint else ''; sys.stderr.write(msg + '\\\\n') if msg else None; sys.exit(0)\""
                - type: "command"
                  command: "python3 -c \"import json, sys; data=json.load(sys.stdin); cmd=data.get('tool_input',{}).get('command',''); is_dangerous='rm -rf /' in cmd; msg='❌ BLOCKED: Dangerous rm command' if is_dangerous else ''; sys.stderr.write(msg + '\\\\n') if msg else None; sys.exit(2 if msg else 0)\""
```

### With additional settings

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.claude_code
      vars:
        claude_code_hooks: []
        claude_code_additional_settings:
          maxTokens: 8192
          model: "claude-sonnet-4.5"
```

## Integration with Fabric

The default hooks block direct `git commit -m` and `gh pr create` commands, requiring you to use Fabric to generate messages first.

Requirements for default hooks:

1. Install Fabric using the `cowdogmoo.workstation.fabric` role
2. Fabric's `commit` pattern (comes with Fabric by default)
3. Hooks will block commits/PRs until you generate messages with Fabric

## File Locations

- **User settings**: `~/.claude/settings.json` - Applies to all projects
- **Project settings**: `.claude/settings.json` - Version-controlled team settings
- **Local settings**: `.claude/settings.local.json` - Personal preferences

This role manages the user-level settings by default.

## Backup

When `claude_code_backup_settings` is enabled (default), the role will automatically create a timestamped backup of your existing settings only when changes are made. This ensures idempotency - backups are only created when the content actually changes. Backups are stored in the same directory with a timestamp suffix.

## License

MIT

## Author Information

This role was created by CowDogMoo.

## References

- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks-guide)
- [Claude Code Configuration Guide](https://www.eesel.ai/blog/settings-json-claude-code)
- [Fabric AI Framework](https://github.com/danielmiessler/fabric)
