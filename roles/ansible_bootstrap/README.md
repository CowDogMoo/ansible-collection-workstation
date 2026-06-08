<!-- DOCSIBLE START -->
# ansible_bootstrap

## Description

Templates ~/.ansible.cfg and creates the ~/.ansible directory tree (collections, roles, fact_cache) plus the remote tmp directory.

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `ansible_bootstrap_user_home` | str | <code>{{ ansible_facts&#91;'env'&#93;&#91;'HOME'&#93; }}</code> | No description |
| `ansible_bootstrap_dir` | str | <code>{{ ansible_bootstrap_user_home }}/.ansible</code> | No description |
| `ansible_bootstrap_collections_path` | str | <code>{{ ansible_bootstrap_dir }}/collections</code> | No description |
| `ansible_bootstrap_roles_path` | str | <code>{{ ansible_bootstrap_dir }}/roles</code> | No description |
| `ansible_bootstrap_fact_cache_path` | str | <code>{{ ansible_bootstrap_dir }}/fact_cache</code> | No description |
| `ansible_bootstrap_remote_tmp` | str | <code>/tmp/.ansible/tmp</code> | No description |
| `ansible_bootstrap_log_folder` | str | <code>{{ ansible_bootstrap_user_home }}/ansible-logs/hosts</code> | No description |
| `ansible_bootstrap_vault_password_file` | str | <code>{{ ansible_bootstrap_dir }}/vault-pass.sh</code> | No description |
| `ansible_bootstrap_install_vault_helper` | bool | <code>True</code> | No description |
| `ansible_bootstrap_manage_cfg` | bool | <code>True</code> | No description |
| `ansible_bootstrap_backup_cfg` | bool | <code>True</code> | No description |

## Tasks

### main.yml


- **Ensure ansible state directories exist** (ansible.builtin.file)
- **Ensure remote tmp directory exists** (ansible.builtin.file)
- **Install vault password helper** (ansible.builtin.copy) - Conditional
- **Render ~/.ansible.cfg** (ansible.builtin.template) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - ansible_bootstrap
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: all
- Kali: all
- EL: all
- macOS: all
<!-- DOCSIBLE END -->
