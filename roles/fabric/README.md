<!-- DOCSIBLE START -->
# fabric

## Description

Installs and configures Daniel Miessler's Fabric AI framework

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `fabric_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `fabric_usergroup` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('staff', fabric_username) }}</code> | No description |
| `fabric_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `fabric_install` | bool | <code>True</code> | No description |
| `fabric_install_method` | str | <code>go_install</code> | No description |
| `fabric_go_package` | str | <code>github.com/danielmiessler/fabric/cmd/fabric@latest</code> | No description |
| `fabric_config_dir` | str | <code>{{ fabric_user_home }}/.config/fabric</code> | No description |
| `fabric_run_setup` | bool | <code>False</code> | No description |
| `fabric_init_directories` | bool | <code>True</code> | No description |
| `fabric_install_custom_patterns` | bool | <code>False</code> | No description |
| `fabric_custom_patterns_repo` | str | <code>https://github.com/CowDogMoo/fabric-patterns-hub</code> | No description |
| `fabric_custom_patterns_version` | str | <code>main</code> | No description |
| `fabric_custom_patterns_subdir` | str | <code>patterns</code> | No description |
| `fabric_custom_patterns_symlink` | bool | <code>False</code> | No description |
| `fabric_update_custom_patterns` | bool | <code>False</code> | No description |

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
- **Determine if patterns source is local or remote** (ansible.builtin.set_fact)
- **Install or update custom patterns** (block) - Conditional
- **Expand local path if tilde is used** (ansible.builtin.set_fact) - Conditional
- **Ensure git is installed (for remote repositories)** (ansible.builtin.package) - Conditional
- **Create temporary directory for custom patterns repository** (ansible.builtin.tempfile) - Conditional
- **Clone custom patterns repository** (ansible.builtin.git) - Conditional
- **Set patterns source directory (remote)** (ansible.builtin.set_fact) - Conditional
- **Set patterns source directory (local)** (ansible.builtin.set_fact) - Conditional
- **Verify patterns source directory exists** (ansible.builtin.stat)
- **Fail if patterns source directory doesn't exist** (ansible.builtin.fail) - Conditional
- **Find all custom pattern directories** (ansible.builtin.find)
- **Create symlinks to custom patterns (for local development)** (ansible.builtin.file) - Conditional
- **Copy custom patterns to fabric patterns directory** (ansible.builtin.copy) - Conditional
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
