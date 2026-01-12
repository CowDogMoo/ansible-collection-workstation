# Claude Code Hooks Configuration Guide

This guide explains how to configure Claude Code hooks using this Ansible role.

## Overview

The role now supports **two types of hooks** for maximum flexibility:

1. **Simple Hooks** - Intuitive YAML configuration (recommended)
2. **Advanced Hooks** - Custom Python/shell scripts for complex logic

## Default Hooks

The role comes pre-configured with these useful hooks:

### 1. Content Validation Hook

Blocks git commits and pull requests that contain emojis or Claude branding, ensuring clean commit messages. Suggests using `fabric` patterns for generating proper commit/PR messages.

### 2. Sound Notifications (macOS)

- **Stop Hook**: Plays 2 beeps when Claude finishes a task or stops working
- **Notification Hook**: Plays 1 beep when Claude needs your input

These hooks help you stay aware of Claude's status without constantly watching the terminal. They use macOS's built-in `osascript` beep functionality.

### Customizing Sound Notifications

To disable sound notifications, override the default hooks in your playbook:

```yaml
- hosts: localhost
  vars:
    claude_code_advanced_hooks:
      # Keep only the content validation hook
      - event: PreToolUse
        tool: Bash
        type: command
        command: |
          python3 -c "..."
  roles:
    - claude_code
```

To use custom sounds (macOS), replace the beep commands:

```yaml
claude_code_advanced_hooks:
  - event: Stop
    tool: ""
    type: command
    command: "afplay /System/Library/Sounds/Glass.aiff"
  - event: Notification
    tool: ""
    type: command
    command: "afplay /System/Library/Sounds/Ping.aiff"
```

## Simple Hooks (Recommended)

Simple hooks require no coding knowledge. Just specify what to match and what message to display.

### Basic Structure

```yaml
claude_code_simple_hooks:
  - name: "Descriptive name"
    event: PreToolUse              # When to trigger
    tool: Bash                      # Which tool to watch
    action: block                   # notify or block
    message: "Your message here"
    # Matching (pick one):
    command_contains: "text"        # Simple string search
    command_pattern: 'regex'        # Regex pattern
    exclude_pattern: "exclude"      # Optional: don't match if contains this
```

### Fields Reference

| Field | Required | Options | Description |
| ------- | ---------- | --------- | ------------- |
| `name` | No | any string | Descriptive name for the hook |
| `event` | No | `PreToolUse`, `PostToolUse`, `UserPromptSubmit` | When to trigger (default: `PreToolUse`) |
| `tool` | No | `Bash`, `Edit`, `Write`, `Read`, etc. | Which tool to watch (default: `Bash`) |
| `action` | Yes | `notify`, `block` | Notify user or block action |
| `message` | Yes | any string (can be multiline) | Message to display |
| `command_contains` | One of these | any string | Simple string search in command |
| `command_pattern` | One of these | regex pattern | Regex pattern to match |
| `exclude_pattern` | No | any string | Don't match if command contains this |

### Quick Examples

```yaml
claude_code_simple_hooks:
  # Simple notification
  - name: "Test hook"
    action: notify
    message: "🔔 Hooks working!"

  # Block dangerous commands
  - name: "Block rm -rf"
    command_contains: "rm -rf /"
    action: block
    message: "Dangerous command blocked!"

  # Pattern matching with exclusion
  - name: "Require linter"
    command_pattern: 'git\s+commit'
    exclude_pattern: 'lint'
    action: block
    message: "Run linter first!"
```

## Advanced Hooks (Custom Logic)

For complex scenarios, use advanced hooks with custom Python or shell scripts.

### Structure

```yaml
claude_code_advanced_hooks:
  - event: PreToolUse
    tool: Bash
    type: command
    command: "your command here"
```

### Example: Inline Python

```yaml
claude_code_advanced_hooks:
  - event: PreToolUse
    tool: Bash
    type: command
    command: |
      python3 -c "
      import json, sys, re

      data = json.load(sys.stdin)
      cmd = data.get('tool_input', {}).get('command', '')

      if 'dangerous' in cmd:
          sys.stderr.write('⚠️  Warning\n')
          sys.exit(2)  # 2 = block
      "
```

### Example: External Script

```yaml
claude_code_advanced_hooks:
  - event: PreToolUse
    tool: Bash
    type: command
    command: "python3 ~/.claude/hooks/custom_validator.py"
```

## Exit Codes

Your hooks should exit with these codes:

- **0** - Success, allow the action
- **1** - Error occurred
- **2** - Block the action

## How It Works

The role converts simple YAML hooks to Python commands automatically. You write simple configuration, the template generates the complex Python logic.

## Pattern Matching

- **command_contains**: Exact string match (`"git commit"`, `"--force"`)
- **command_pattern**: Regex (`'git\s+commit'`, `'rm\s+-rf?\s+/'`)
- **exclude_pattern**: Skip if contains string (`'fabric'`, `'lint'`)

**Regex tips**: `\s+` = spaces, `.*` = any chars, `\d+` = numbers

## Common Use Cases

### 1. Enforce Workflow Tools

```yaml
- name: "Use fabric for commits"
  command_pattern: 'git\s+commit.*-m'
  exclude_pattern: 'fabric'
  action: block
  message: "Generate commit messages with fabric"
```

### 2. Safety Checks

```yaml
- name: "Protect main branch"
  command_pattern: 'git\s+push.*main'
  action: block
  message: "Don't push directly to main - create a PR"

- name: "Warn about sudo"
  command_contains: "sudo rm"
  action: notify
  message: "⚠️  Be careful with sudo rm"
```

### 3. Code Quality Gates

```yaml
- name: "Run tests"
  command_contains: "git push"
  action: notify
  message: "Remember to run tests: npm test"

- name: "Lint before commit"
  command_pattern: 'git\s+commit'
  exclude_pattern: 'lint'
  action: block
  message: "Run linter first: npm run lint"
```

### 4. Reminders

```yaml
- name: "Update changelog"
  command_contains: "npm version"
  action: notify
  message: "📝 Don't forget to update CHANGELOG.md"
```

## Debugging

**Test hook system:**

```yaml
- action: notify
  message: "🔔 Hooks working!"
```

**Check config:** `cat ~/.claude/settings.json`

**Not triggering?**

1. Pattern doesn't match command
2. Wrong tool (default: `Bash`)
3. Test regex: `echo "cmd" | grep -E 'pattern'`

## Disabling Hooks

```yaml
# Disable all
claude_code_simple_hooks: []
claude_code_advanced_hooks: []

# Comment out specific hooks
claude_code_simple_hooks:
  - name: "Active"
    action: notify
    message: "Runs"
  # - name: "Disabled"
  #   action: block
```

## Further Reading

- **`files/hook_examples.yml`** - Comprehensive examples collection
- **`files/hook_helpers.py`** - Reusable Python functions
- **[Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks-guide)**
- **[Role README](../README.md)** - Full role documentation

## Contributing

Have a useful hook pattern? Consider contributing it to `files/hook_examples.yml`!
