<!-- DOCSIBLE START -->
# shell_functions

## Description

Deploys the user's dotfiles shell-function library to ~/.dotfiles

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `shell_functions_user_home` | str | <code>{{ ansible_facts&#91;'env'&#93;&#91;'HOME'&#93; }}</code> | No description |
| `shell_functions_dest` | str | <code>{{ shell_functions_user_home }}/.dotfiles</code> | No description |
| `shell_functions_source_path` | str | <code></code> | No description |
| `shell_functions_repo_url` | str | <code>https://github.com/l50/dotfiles.git</code> | No description |
| `shell_functions_repo_version` | str | <code>main</code> | No description |
| `shell_functions_cache_path` | str | <code>{{ shell_functions_user_home }}/.cache/cowdogmoo/shell_functions</code> | No description |
| `shell_functions_payload` | list | <code>&#91;&#93;</code> | No description |
| `shell_functions_payload.0` | str | <code>android.sh</code> | No description |
| `shell_functions_payload.1` | str | <code>bashutils.sh</code> | No description |
| `shell_functions_payload.2` | str | <code>cloud</code> | No description |
| `shell_functions_payload.3` | str | <code>common.sh</code> | No description |
| `shell_functions_payload.4` | str | <code>config</code> | No description |
| `shell_functions_payload.5` | str | <code>containers.sh</code> | No description |
| `shell_functions_payload.6` | str | <code>docker.sh</code> | No description |
| `shell_functions_payload.7` | str | <code>files</code> | No description |
| `shell_functions_payload.8` | str | <code>git.sh</code> | No description |
| `shell_functions_payload.9` | str | <code>go.sh</code> | No description |
| `shell_functions_payload.10` | str | <code>k8s.sh</code> | No description |
| `shell_functions_payload.11` | str | <code>macos.sh</code> | No description |
| `shell_functions_payload.12` | str | <code>op.sh</code> | No description |
| `shell_functions_payload.13` | str | <code>python.sh</code> | No description |
| `shell_functions_payload.14` | str | <code>ssh-agent.sh</code> | No description |
| `shell_functions_payload.15` | str | <code>terraform.sh</code> | No description |

## Tasks

### main.yml


- **Check whether the local source path exists** (ansible.builtin.stat) - Conditional
- **Decide whether to use the local checkout** (ansible.builtin.set_fact)
- **Ensure destination directory exists** (ansible.builtin.file)
- **Ensure cache parent directory exists** (ansible.builtin.file) - Conditional
- **Maintain cached clone of dotfiles repo** (ansible.builtin.git) - Conditional
- **Resolve effective source directory** (ansible.builtin.set_fact)
- **Copy payload items into destination** (ansible.builtin.copy)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - shell_functions
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
