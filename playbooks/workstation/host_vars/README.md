# Host-Specific Variables

This directory contains host-specific variable overrides for the workstation playbook.

## How It Works

Ansible automatically loads variables from files matching the hostname:

- When running on `ouroboros`, it loads `ouroboros.yml`
- When running on your work machine, create a file named `{hostname}.yml`

## Setup for a New Machine

1. Get your machine's hostname:

   ```bash
   hostname
   ```

2. Create a file named `{hostname}.yml` in this directory

3. Copy the content from `MacBook-Pro-4.yml` or `ouroboros.yml` as a template and customize

4. Run your dotfiles installer:

   ```bash
   ~/dotfiles/install_dot_files.sh
   ```

## Example: Custom Sound Notifications

Each machine can have different sound files:

**Personal machine** (ouroboros):

```yaml
command: "afplay \"$HOME/Jobs Done.mp3\""
```

**Work machine**:

```yaml
command: "afplay \"$HOME/work-sound.mp3\""
```

**Fall back to default** (system beep):

```yaml
command: "osascript -e 'beep 2'"
```

## Priority

Variables are loaded in this order (last wins):

1. `roles/claude_code/defaults/main.yml` - Default for all machines
2. `playbooks/workstation/host_vars/{hostname}.yml` - This machine's overrides
3. Extra vars passed on command line

## Adding New Overrides

You can override any variable from `roles/claude_code/defaults/main.yml`:

- `claude_code_install`
- `claude_code_manage_settings`
- `claude_code_simple_hooks`
- `claude_code_advanced_hooks`
- `claude_code_additional_settings`
