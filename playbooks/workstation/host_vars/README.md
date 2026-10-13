# Host-Specific Variables

This directory contains host-specific variable overrides for the workstation playbook.

## How It Works

Ansible loads variables from the entry matching the **inventory hostname**,
either a file (`{hostname}.yml`) or a directory (`{hostname}/`):

- When the inventory host is `ouroboros`, it loads `ouroboros.yml`
- When the inventory host is `MacBook-Pro-4`, it loads every file in `MacBook-Pro-4/`

The inventory hostname is whatever the run targets, not the machine's real
hostname. A run with no inventory targets `localhost`, which matches nothing
here, so the workstation playbook stops with an error rather than rewriting
your config from role defaults.

## Running for This Machine

From the repo root, target the machine by its short hostname:

```bash
ansible-playbook playbooks/workstation/workstation.yml -i "$(hostname -s)," -c local
```

Add `--tags claude` (or any other role tag) to run a single role. The dotfiles
installer (`~/dotfiles/install_dot_files.sh`) passes the hostname for you.

## Setup for a New Machine

1. Get your machine's short hostname:

   ```bash
   hostname -s
   ```

2. Create a file named `{hostname}.yml` (or a `{hostname}/` directory) here

3. Copy the content from `MacBook-Pro-4/` or `ouroboros.yml` as a template and customize

4. Run the playbook for this machine (command above), or your dotfiles installer:

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
2. `playbooks/workstation/host_vars/{hostname}.yml` (or `{hostname}/`) - This machine's overrides
3. Extra vars passed on command line

## Adding New Overrides

You can override any variable from `roles/claude_code/defaults/main.yml`:

- `claude_code_install`
- `claude_code_manage_settings`
- `claude_code_simple_hooks`
- `claude_code_advanced_hooks`
- `claude_code_additional_settings`
