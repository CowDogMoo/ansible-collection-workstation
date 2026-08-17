<!-- DOCSIBLE START -->
# logging

## Description

Provides flexible logging directories and log rotation for any application or service.

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `logging_directories` | list | <code>&#91;&#93;</code> | No description |
| `logging_rotation_configs` | list | <code>&#91;&#93;</code> | No description |
| `logging_launchagent_label` | str | <code>com.logging.logrotate</code> | No description |
| `logging_launchagent_hour` | int | <code>3</code> | No description |
| `logging_launchagent_minute` | int | <code>0</code> | No description |
| `logging_logrotate_log_path` | str | <code>{{ (ansible_facts&#91;'user_dir'&#93; &#124; default(ansible_facts&#91;'env'&#93;&#91;'HOME'&#93;)) }}/logs/logrotate</code> | No description |
| `logging_manage_system` | bool | <code>False</code> | No description |
| `logging_systemd_timer_on_calendar` | str | <code>*-*-* 03:00:00</code> | No description |
| `logging_logrotate_binary_darwin` | str | <code>/opt/homebrew/sbin/logrotate</code> | No description |
| `logging_logrotate_binary_linux` | str | <code>/usr/sbin/logrotate</code> | No description |
| `logging_logrotate_config_dir_darwin` | str | <code>{{ (ansible_facts&#91;'user_dir'&#93; &#124; default(ansible_facts&#91;'env'&#93;&#91;'HOME'&#93;)) }}/.config/logrotate.d</code> | No description |
| `logging_logrotate_config_dir_linux` | str | <code>{{ '/etc/logrotate.d' if (ansible_facts&#91;'user_id'&#93; == 'root' or logging_manage_system &#124; bool) else ((ansible_facts&#91;'user_dir'&#93; &#124; default(ansible_facts&#91;'env'&#93;&#91;'HOME'&#93;)) + '/.config/logrotate.d') }}</code> | No description |
| `logging_logrotate_state_file` | str | <code>{{ (ansible_facts&#91;'user_dir'&#93; &#124; default(ansible_facts&#91;'env'&#93;&#91;'HOME'&#93;)) + '/.config/logrotate.state' if (ansible_facts&#91;'os_family'&#93; == 'Darwin' or ansible_facts&#91;'user_id'&#93; != 'root') else '/var/lib/logrotate/status' }}</code> | No description |
| `logging_logrotate_binary` | str | <code>{{ logging_logrotate_binary_darwin if ansible_facts&#91;'os_family'&#93; == 'Darwin' else logging_logrotate_binary_linux }}</code> | No description |
| `logging_logrotate_config_dir` | str | <code>{{ logging_logrotate_config_dir_darwin if ansible_facts&#91;'os_family'&#93; == 'Darwin' else logging_logrotate_config_dir_linux }}</code> | No description |

## Tasks

### main.yml


- **Set OS-specific facts** (ansible.builtin.set_fact)
- **Check if logrotate binary exists** (ansible.builtin.stat)
- **Install logrotate on macOS** (community.general.homebrew) - Conditional
- **Install logrotate on Linux (Debian-based)** (ansible.builtin.apt) - Conditional
- **Install logrotate on Linux (RedHat-based)** (ansible.builtin.dnf) - Conditional
- **Ensure logging directories exist** (ansible.builtin.file) - Conditional
- **Ensure parent directory for logrotate config exists on macOS** (ansible.builtin.file) - Conditional
- **Ensure logrotate config directory exists** (ansible.builtin.file) - Conditional
- **Ensure olddir directories exist for log rotation** (ansible.builtin.file)
- **Setup log rotation configurations** (ansible.builtin.template) - Conditional
- **Ensure logrotate state directory exists on macOS** (ansible.builtin.file) - Conditional
- **Create logrotate state file on macOS** (ansible.builtin.file) - Conditional
- **Create LaunchAgent directory on macOS** (ansible.builtin.file) - Conditional
- **Create LaunchAgent for logrotate on macOS** (ansible.builtin.template) - Conditional
- **Unload existing LaunchAgent if present** (ansible.builtin.command) - Conditional
- **Load LaunchAgent for logrotate on macOS** (ansible.builtin.command) - Conditional
- **Ensure logrotate's own log directory exists** (ansible.builtin.file) - Conditional
- **Ensure systemd user unit directory exists** (ansible.builtin.file) - Conditional
- **Install systemd user units for logrotate** (ansible.builtin.template) - Conditional
- **Check for a reachable systemd user session** (ansible.builtin.command) - Conditional
- **Enable and start the logrotate user timer** (ansible.builtin.systemd_service) - Conditional

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
