<!-- DOCSIBLE START -->
# zsh_setup

## Description

Installs and configures zsh with oh-my-zsh.

## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.package_management

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| ---------- | ------ | --------- | ------------- |
| `zsh_setup_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) &#124; default(ansible_facts&#91;'distribution'&#93; &#124; lower) }}</code> | No description |
| `zsh_setup_usergroup` | str | <code>{{ 'staff' if ansible_facts&#91;'os_family'&#93; == 'Darwin' else 'Administrators' if ansible_facts&#91;'os_family'&#93; == 'Windows' else zsh_setup_username }}</code> | No description |
| `zsh_setup_shell` | str | <code>{{ 'powershell' if ansible_facts&#91;'os_family'&#93; == 'Windows' else (ansible_facts&#91;'env'&#93;&#91;'SHELL'&#93; &#124; default('/bin/bash')).strip() &#124; regex_replace('\n', '') }}</code> | No description |
| `zsh_setup_theme` | str | <code>af-magic</code> | No description |
| `zsh_setup_plugins` | list | <code>&#91;&#93;</code> | No description |
| `zsh_setup_plugins.0` | str | <code>asdf</code> | No description |
| `zsh_setup_plugins.1` | str | <code>aws</code> | No description |
| `zsh_setup_plugins.2` | str | <code>git</code> | No description |
| `zsh_setup_plugins.3` | str | <code>docker</code> | No description |
| `zsh_setup_plugins.4` | str | <code>helm</code> | No description |
| `zsh_setup_plugins.5` | str | <code>kubectl</code> | No description |
| `zsh_setup_plugins.6` | str | <code>zsh-completions</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| ---------- | ------ | ------- | ------------- |
| `zsh_setup_common_install_packages` | list | `[]` | No description |
| `zsh_setup_common_install_packages.0` | str | `zsh` | No description |
| `zsh_setup_common_install_packages.1` | str | `zsh-autosuggestions` | No description |
| `zsh_setup_omz_install_script_url` | str | `https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh` | No description |

## Tasks

### common.yml

- **Ensure user home directory exists** (ansible.builtin.include_tasks) - Conditional
- **Check if oh-my-zsh exists** (ansible.builtin.stat)
- **Download oh-my-zsh install script** (ansible.builtin.get_url) - Conditional
- **Check for bash** (ansible.builtin.command)
- **Set shell executable** (ansible.builtin.set_fact)
- **Install oh-my-zsh** (ansible.builtin.shell) - Conditional
- **Remove omz-installer.sh** (ansible.builtin.file) - Conditional
- **Check if .zshrc exists** (ansible.builtin.stat)
- **Ensure .zshrc exists** (ansible.builtin.template) - Conditional

### main.yml

- **Include tasks to get user home directory** (ansible.builtin.include_tasks)
- **Install required packages for zsh** (ansible.builtin.include_role)
- **Ensure user group exists** (ansible.builtin.group) - Conditional
- **Ensure user exists** (ansible.builtin.user) - Conditional
- **Include common tasks** (ansible.builtin.include_tasks)

### zsh_setup_get_user_home.yml

- **Gather available local users** (ansible.builtin.getent) - Conditional
- **Gather available local users on macOS** (cowdogmoo.workstation.getent_passwd) - Conditional
- **Set user home directory** (ansible.builtin.set_fact) - Conditional
- **Set user home directory for macOS** (ansible.builtin.set_fact) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - zsh_setup
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms

- Ubuntu: all
- macOS: all
<!-- DOCSIBLE END -->
