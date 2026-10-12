<!-- DOCSIBLE START -->
# firstmate

## Description

Installs the firstmate agent distro by cloning its repository, without configuring fleet homes or starting sessions

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `firstmate_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `firstmate_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `firstmate_repo_url` | str | <code>https://github.com/kunchenguid/firstmate.git</code> | No description |
| `firstmate_version` | str | <code>main</code> | No description |
| `firstmate_install_dir` | str | <code>{{ firstmate_user_home }}/firstmate</code> | No description |
| `firstmate_update` | bool | <code>False</code> | No description |
| `firstmate_manage_dependencies` | bool | <code>True</code> | No description |
| `firstmate_dependencies` | list | <code>&#91;&#93;</code> | No description |
| `firstmate_dependencies.0` | str | <code>git</code> | No description |
| `firstmate_dependencies.1` | str | <code>jq</code> | No description |

## Tasks

### main.yml


- **Install firstmate dependencies** (ansible.builtin.package) - Conditional
- **Check for an existing firstmate checkout** (ansible.builtin.stat)
- **Clone firstmate** (ansible.builtin.git) - Conditional
- **Display firstmate checkout** (ansible.builtin.debug)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - firstmate
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
