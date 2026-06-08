<!-- DOCSIBLE START -->
# git_setup

## Description

Renders ~/.gitconfig with aliases and sane defaults

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `git_setup_user_home` | str | <code>{{ ansible_facts&#91;'env'&#93;&#91;'HOME'&#93; }}</code> | No description |
| `git_setup_gitconfig_path` | str | <code>{{ git_setup_user_home }}/.gitconfig</code> | No description |
| `git_setup_userparams_path` | str | <code>{{ git_setup_user_home }}/.gitconfig.userparams</code> | No description |
| `git_setup_editor` | str | <code>code --wait</code> | No description |
| `git_setup_push_default` | str | <code>matching</code> | No description |
| `git_setup_pull_rebase` | bool | <code>True</code> | No description |
| `git_setup_gh_credential_helper` | bool | <code>True</code> | No description |
| `git_setup_backup` | bool | <code>True</code> | No description |

## Tasks

### main.yml


- **Render ~/.gitconfig** (ansible.builtin.template)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - git_setup
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: all
- Debian: all
- EL: all
- Fedora: all
- MacOSX: all
<!-- DOCSIBLE END -->
