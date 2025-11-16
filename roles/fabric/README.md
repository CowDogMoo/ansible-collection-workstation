<!-- DOCSIBLE START -->
# fabric

## Description

Installs and configures Daniel Miessler's Fabric AI framework

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `fabric_username` | str | `{{ ansible_facts['user_id'] \| default(ansible_facts['user']) }}` | No description |
| `fabric_usergroup` | str | `{{ (ansible_facts['os_family'] == 'Darwin') \| ternary('staff', fabric_username) }}` | No description |
| `fabric_user_home` | str | `<multiline value: folded_strip>` | No description |
| `fabric_install` | bool | `True` | No description |
| `fabric_install_method` | str | `go_install` | No description |
| `fabric_go_package` | str | `github.com/danielmiessler/fabric/cmd/fabric@latest` | No description |
| `fabric_config_dir` | str | `{{ fabric_user_home }}/.config/fabric` | No description |
| `fabric_run_setup` | bool | `False` | No description |
| `fabric_init_directories` | bool | `True` | No description |
| `fabric_install_custom_patterns` | bool | `False` | No description |
| `fabric_custom_patterns_repo` | str | `https://github.com/CowDogMoo/fabric-patterns-hub` | No description |
| `fabric_custom_patterns_version` | str | `main` | No description |
| `fabric_custom_patterns_subdir` | str | `patterns` | No description |
| `fabric_update_custom_patterns` | bool | `False` | No description |

## Tasks

### install-go.yml

- **Check if fabric is already installed** (ansible.builtin.command)
- **Check if Go is available** (ansible.builtin.command) - Conditional
- **Fail if Go is not available** (ansible.builtin.fail) - Conditional
- **Install Fabric via go install** (ansible.builtin.shell) - Conditional
- **Verify fabric installation** (ansible.builtin.command)
- **Display installed version** (ansible.builtin.debug) - Conditional

### install-homebrew.yml

- **Check if running on macOS** (ansible.builtin.fail) - Conditional
- **Check if fabric is already installed** (ansible.builtin.command)
- **Install Fabric via Homebrew** (community.general.homebrew) - Conditional
- **Verify fabric installation** (ansible.builtin.command)
- **Display installed version** (ansible.builtin.debug)

### install-npm.yml

- **Check if fabric is already installed** (ansible.builtin.command)
- **Check if npm is available** (ansible.builtin.command) - Conditional
- **Fail if npm is not available** (ansible.builtin.fail) - Conditional
- **Install Fabric via npm** (community.general.npm) - Conditional
- **Verify fabric installation** (ansible.builtin.command)
- **Display installed version** (ansible.builtin.debug) - Conditional

### install-script.yml

- **Check if fabric is already installed** (ansible.builtin.stat)
- **Install Fabric via official install script** (ansible.builtin.shell) - Conditional
- **Verify fabric installation** (ansible.builtin.command)
- **Display installed version** (ansible.builtin.debug) - Conditional

### main.yml

- **Set fabric username for Kali systems** (ansible.builtin.set_fact) - Conditional
- **Ensure fabric user home directory exists** (ansible.builtin.stat)
- **Fail if user home directory doesn't exist** (ansible.builtin.fail) - Conditional
- **Install Fabric** (block) - Conditional
- **Install Fabric via go install** (ansible.builtin.include_tasks) - Conditional
- **Install Fabric via install script** (ansible.builtin.include_tasks) - Conditional
- **Install Fabric via Homebrew** (ansible.builtin.include_tasks) - Conditional
- **Install Fabric via npm** (ansible.builtin.include_tasks) - Conditional
- **Create fabric configuration directory** (ansible.builtin.file) - Conditional
- **Create fabric patterns directory** (ansible.builtin.file) - Conditional
- **Manage custom patterns from git repository** (ansible.builtin.include_tasks) - Conditional
- **Display fabric installation status** (ansible.builtin.debug)

### manage-custom-patterns.yml

- **Check if custom patterns marker file exists** (ansible.builtin.stat) - Conditional
- **Determine if custom patterns should be installed or updated** (ansible.builtin.set_fact)
- **Install or update custom patterns** (block) - Conditional
- **Ensure git is installed** (ansible.builtin.package)
- **Create temporary directory for custom patterns repository** (ansible.builtin.tempfile)
- **Clone custom patterns repository** (ansible.builtin.git)
- **Find all custom pattern directories** (ansible.builtin.find)
- **Copy custom patterns to fabric patterns directory** (ansible.builtin.copy)
- **Create marker file to track installation** (ansible.builtin.copy)
- **Clean up temporary directory** (ansible.builtin.file) - Conditional
- **Display custom patterns installation status** (ansible.builtin.debug) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - fabric
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
