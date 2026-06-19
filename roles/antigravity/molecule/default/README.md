# Molecule Tests for Antigravity Role

This directory contains Molecule tests for the `antigravity` role, testing the installation and configuration of Antigravity CLI.

## Test Scenarios

### Multi-Platform Testing

Tests are executed on multiple platforms:

- **Ubuntu 22.04** (`ubuntu-agy-code`) - Ubuntu LTS
- **Kali Linux** (`kali-agy-code`) - Debian-based security distribution

## What is Tested

### 1. Installation

- ✅ Antigravity CLI is installed
- ✅ Binary is accessible in PATH
- ✅ Version command works correctly

### 2. Configuration Directory

- ✅ Config directory (`~/.gemini/config`) is created
- ✅ Directory has correct permissions (0755)
- ✅ Directory has correct ownership

### 3. Settings Management

- ✅ settings.json is created
- ✅ File has correct permissions (0644)
- ✅ File has correct ownership
- ✅ Settings contain valid JSON

### 4. Simple Hooks Configuration

- ✅ Simple hooks are converted to proper Antigravity format
- ✅ `command_contains` pattern matching works
- ✅ `command_pattern` regex matching works
- ✅ `exclude_pattern` filtering works
- ✅ `action` (notify/block) is correctly converted to exit codes
- ✅ Messages are properly embedded in Python commands
- ✅ All hooks have correct structure (matcher, hooks array)

### 5. Advanced Hooks Configuration

- ✅ Advanced hooks are preserved as-is
- ✅ Custom Python commands are included correctly
- ✅ Mixed simple and advanced hooks work together
- ✅ Hooks are properly grouped by event and tool

### 6. Edge Cases

- ✅ Empty hooks configuration (no hooks at all)
- ✅ Simple hooks only (no advanced hooks)
- ✅ Advanced hooks only (no simple hooks)
- ✅ Mixed hooks (both simple and advanced)

### 7. Backup Functionality

- ✅ Backup files are created when settings exist
- ✅ Backups use timestamped naming

### 8. Idempotency

- ✅ Role runs twice without changes on second run
- ✅ Demonstrates proper Ansible idempotency

## Running the Tests

```bash
# Run all tests
cd roles/antigravity
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
molecule test -s default -- --platform-name ubuntu-agy-code
```

## Test Dependencies

The prepare phase installs:

- Node.js 18+
- npm

These are required for Antigravity CLI installation via npm.

## Expected Outcomes

All tests should pass, demonstrating that:

1. Antigravity CLI is properly installed on both Ubuntu and Kali
2. Configuration is correctly generated in `~/.gemini/config/settings.json`
3. Simple hooks are converted to Antigravity JSON format correctly
4. Advanced hooks are preserved and mixed with simple hooks
5. All hook patterns (contains, regex, exclude) work correctly
6. Edge cases (empty, simple-only, advanced-only) are handled
7. Files have correct permissions and ownership
8. The role is fully idempotent
9. Backups are created when appropriate

## Hook Testing Details

Tests verify simple hooks are converted to Python commands with:

- Proper `hooks.PreToolUse` JSON structure
- Correct `matcher` field
- Pattern matching logic embedded
- Messages properly escaped
- Correct exit codes (0=notify, 2=block)

## Troubleshooting

If tests fail:

1. **Installation failures**: Check if npm is available in the container
2. **Permission errors**: Verify user/group settings in converge.yml
3. **Path issues**: Ensure PATH includes npm global bin directory
4. **JSON parsing errors**: Validate settings.json template syntax
