<!-- DOCSIBLE START -->
# logging

## Description

Provides logging directories and log rotation for other roles.

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `logging_directories` | list | `[]` | No description |
| `logging_directories.0` | dict | `{}` | No description |
| `logging_log_rotation_config` | dict | `{}` | No description |
| `logging_log_rotation_config.path` | str | `/var/log/ansible/*.log` | No description |
| `logging_log_rotation_config.rotate` | int | `4` | No description |
| `logging_log_rotation_config.frequency` | str | `weekly` | No description |
| `logging_log_rotation_config.compress` | bool | `True` | No description |
| `logging_log_rotation_config.missingok` | bool | `True` | No description |
| `logging_log_rotation_config.notifempty` | bool | `True` | No description |
| `logging_log_rotation_config.create` | bool | `True` | No description |
| `logging_log_rotation_config.dateext` | bool | `True` | No description |
| `logging_log_rotation_config.owner` | str | `root` | No description |
| `logging_log_rotation_config.group` | str | `root` | No description |

## Tasks

### main.yml

- **Ensure logging directories exist** (ansible.builtin.file)
- **Setup log rotation** (ansible.builtin.template)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - logging
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms

- Ubuntu: all
- Kali: all
- EL: all
<!-- DOCSIBLE END -->
