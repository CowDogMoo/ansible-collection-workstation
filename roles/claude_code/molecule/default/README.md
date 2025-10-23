# Molecule Tests for Claude Code Role

This directory contains Molecule tests for the `claude_code` role, testing the installation and configuration of Claude Code CLI.

## Test Scenarios

### Multi-Platform Testing

Tests are executed on multiple platforms:

- **Ubuntu 22.04** (`ubuntu-claude-code`) - Ubuntu LTS
- **Kali Linux** (`kali-claude-code`) - Debian-based security distribution

## What is Tested

### 1. Installation

- ✅ Claude Code CLI is installed
- ✅ Binary is accessible in PATH
- ✅ Version command works correctly

### 2. Configuration Directory

- ✅ Config directory (`~/.config/claude`) is created
- ✅ Directory has correct permissions (0755)
- ✅ Directory has correct ownership

### 3. Settings Management

- ✅ settings.json is created
- ✅ File has correct permissions (0644)
- ✅ File has correct ownership
- ✅ Settings contain valid JSON

### 4. Hooks Configuration

- ✅ Hooks array is present in settings
- ✅ All hooks have required fields (name, event, matchers, command)
- ✅ Custom test hook is properly configured
- ✅ Matchers contain tool and pattern

### 5. Backup Functionality

- ✅ Backup files are created when settings exist
- ✅ Backups use timestamped naming

### 6. Idempotency

- ✅ Role runs twice without changes on second run
- ✅ Demonstrates proper Ansible idempotency

## Running the Tests

```bash
# Run all tests
cd roles/claude_code
molecule test

# Run individual steps
molecule create      # Create test containers
molecule prepare     # Install Node.js and npm
molecule converge    # Apply the role
molecule verify      # Run verification tests
molecule destroy     # Clean up

# Debug mode
molecule converge -- -vvv

# Test on specific platform
molecule test -s default -- --platform-name ubuntu-claude-code
```

## Test Dependencies

The prepare phase installs:

- Node.js 18+
- npm

These are required for Claude Code CLI installation via npm.

## Expected Outcomes

All tests should pass, demonstrating that:

1. Claude Code CLI is properly installed on both Ubuntu and Kali
2. Configuration is correctly generated and placed
3. Hooks are properly configured in settings.json
4. Files have correct permissions and ownership
5. The role is fully idempotent
6. Backups are created when appropriate

## Troubleshooting

If tests fail:

1. **Installation failures**: Check if npm is available in the container
2. **Permission errors**: Verify user/group settings in converge.yml
3. **Path issues**: Ensure PATH includes npm global bin directory
4. **JSON parsing errors**: Validate settings.json template syntax
