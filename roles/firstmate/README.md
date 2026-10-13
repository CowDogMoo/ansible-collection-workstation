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
| `firstmate_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | User who owns the firstmate checkout. |
| `firstmate_user_home` | str | <code><multiline value: folded_strip></code> | Home directory of firstmate_username. |
| `firstmate_repo_url` | str | <code>https://github.com/kunchenguid/firstmate.git</code> | Git repository firstmate is cloned from. |
| `firstmate_version` | str | <code>main</code> | Branch, tag, or commit checked out on the initial clone. |
| `firstmate_install_dir` | str | <code>{{ firstmate_user_home }}/firstmate</code> | Where the firstmate checkout lives. |
| `firstmate_update` | bool | <code>False</code> | Fetch and check out firstmate_version on an existing checkout. |
| `firstmate_manage_dependencies` | bool | <code>True</code> | Install firstmate_dependencies with the system package manager (Linux only). |
| `firstmate_dependencies` | list | <code>&#91;&#93;</code> | Packages installed when firstmate_manage_dependencies is true. |
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
