<!-- DOCSIBLE START -->
# logging

## Description

Provides flexible logging directories and log rotation for any application or service.

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `logging_directories` | list | <code>&#91;&#93;</code> | No description |
| `logging_rotation_configs` | list | <code>&#91;&#93;</code> | No description |
| `logging_launchagent_label` | str | <code>com.logging.logrotate</code> | No description |
| `logging_launchagent_hour` | int | <code>3</code> | No description |
| `logging_launchagent_minute` | int | <code>0</code> | No description |
| `logging_logrotate_log_path` | str | <code>{{ ansible_env.HOME }}/logs/logrotate</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `logging_logrotate_binary_darwin` | str | `/opt/homebrew/sbin/logrotate` | No description |
| `logging_logrotate_binary_linux` | str | `/usr/sbin/logrotate` | No description |
| `logging_logrotate_config_dir_darwin` | str | `{{ ansible_facts['env']['HOME'] }}/.config/logrotate.d` | No description |
| `logging_logrotate_config_dir_linux` | str | `/etc/logrotate.d` | No description |
| `logging_logrotate_state_file` | str | `{{ ansible_facts['env']['HOME'] + '/.config/logrotate.state' if ansible_facts['os_family'] == 'Darwin' else '/var/lib/logrotate/status' }}` | No description |

## Tasks

### main.yml

- **Set OS-specific facts** (ansible.builtin.set_fact)
- **Set logrotate paths based on OS** (ansible.builtin.set_fact)
- **Check if logrotate binary exists** (ansible.builtin.stat)
- **Install logrotate on macOS** (community.general.homebrew) - Conditional
- **Install logrotate on Linux (Debian-based)** (ansible.builtin.apt) - Conditional
- **Install logrotate on Linux (RedHat-based)** (ansible.builtin.dnf) - Conditional
- **Ensure logging directories exist** (ansible.builtin.file) - Conditional
- **Ensure parent directory for logrotate config exists on macOS** (ansible.builtin.file) - Conditional
- **Ensure logrotate config directory exists** (ansible.builtin.file) - Conditional
- **Setup log rotation configurations** (ansible.builtin.template) - Conditional
- **Ensure logrotate state directory exists on macOS** (ansible.builtin.file) - Conditional
- **Create logrotate state file on macOS** (ansible.builtin.file) - Conditional
- **Create LaunchAgent directory on macOS** (ansible.builtin.file) - Conditional
- **Create LaunchAgent for logrotate on macOS** (ansible.builtin.template) - Conditional
- **Unload existing LaunchAgent if present** (ansible.builtin.command) - Conditional
- **Load LaunchAgent for logrotate on macOS** (ansible.builtin.command) - Conditional
- **Ensure logrotate's own log directory exists** (ansible.builtin.file) - Conditional

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
