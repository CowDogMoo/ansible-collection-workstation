<!-- DOCSIBLE START -->
# tmux_setup

## Description

Renders ~/.tmux.conf with mouse-friendly bindings and OSC52 clipboard

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `tmux_setup_user_home` | str | <code>{{ ansible_facts&#91;'env'&#93;&#91;'HOME'&#93; }}</code> | No description |
| `tmux_setup_conf_path` | str | <code>{{ tmux_setup_user_home }}/.tmux.conf</code> | No description |
| `tmux_setup_default_terminal` | str | <code>screen-256color</code> | No description |
| `tmux_setup_clipboard_command` | str | <code>pbcopy</code> | No description |
| `tmux_setup_backup` | bool | <code>True</code> | No description |
| `tmux_setup_local_overrides_path` | str | <code>{{ tmux_setup_user_home }}/.tmux.conf.local</code> | No description |

## Tasks

### main.yml


- **Render ~/.tmux.conf** (ansible.builtin.template)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - tmux_setup
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
