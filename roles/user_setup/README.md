<!-- DOCSIBLE START -->
# user_setup

## Description

Sets up user accounts with optional sudo privileges for Unix-like and Windows systems.

## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.package_management

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `user_setup_default_username` | str | `{{ ansible_facts['distribution'] \| lower }}` | No description |
| `user_setup_default_group` | str | `{{ ansible_facts['distribution'] \| lower }}` | No description |
| `user_setup_default_users` | list | `[]` | No description |
| `user_setup_default_users.0` | dict | `{}` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `user_setup_install_packages` | list | `[]` | No description |
| `user_setup_install_packages.0` | str | `bash` | No description |
| `user_setup_install_packages.1` | str | `sudo` | No description |

## Tasks

### main.yml

- **Gather available local users** (ansible.builtin.getent) - Conditional
- **Gather available local users on macOS** (cowdogmoo.workstation.getent_passwd) - Conditional
- **Normalize getent_passwd structure** (ansible.builtin.set_fact) - Conditional
- **Gather the list of unique shells to install** (ansible.builtin.set_fact) - Conditional
- **Install base packages for all users** (ansible.builtin.include_role) - Conditional
- **Install user-specific shells** (ansible.builtin.package) - Conditional
- **Ensure groups exist for users** (ansible.builtin.group) - Conditional
- **Create users on non-Windows systems** (ansible.builtin.user) - Conditional
- **Ensure users exist and have home directories** (ansible.builtin.user) - Conditional
- **Provide sudoers access for relevant users in sudoers.d** (ansible.builtin.copy) - Conditional
- **Create a new Windows user** (ansible.windows.win_user) - Conditional
- **Ensure specified user groups are in place for Windows** (ansible.windows.win_group_membership) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - user_setup
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms

- Ubuntu: all
- Kali: all
- EL: all
- Windows: all
<!-- DOCSIBLE END -->
