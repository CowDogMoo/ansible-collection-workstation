<!-- DOCSIBLE START -->
# alloy

## Description

Grafana Alloy installation and configuration for macOS

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `alloy_version` | str | `latest` | No description |
| `alloy_config_dir` | str | `/opt/homebrew/etc/alloy` | No description |
| `alloy_config_file` | str | `config.alloy` | No description |
| `alloy_service_name` | str | `alloy` | No description |
| `alloy_user` | str | `{{ ansible_user_id }}` | No description |
| `alloy_group` | str | `{{ ansible_user_gid }}` | No description |
| `alloy_log_level` | str | `debug` | No description |
| `alloy_log_format` | str | `logfmt` | No description |
| `alloy_ansible_logs_path` | str | `{{ ansible_env.HOME }}/ansible-logs/hosts/*` | No description |
| `alloy_ansible_logs_job` | str | `ansible` | No description |
| `alloy_ansible_logs_environment` | str | `local` | No description |
| `alloy_ansible_logs_sync_period` | str | `10s` | No description |
| `alloy_tail_from_end` | bool | `False` | No description |
| `alloy_loki_endpoint` | str | `https://loki.techvomit.xyz/loki/api/v1/push` | No description |
| `alloy_loki_application` | str | `ansible` | No description |
| `alloy_loki_service_name` | str | `ansible` | No description |
| `alloy_service_enabled` | bool | `True` | No description |
| `alloy_service_state` | str | `started` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `alloy_brew_tap` | str | `grafana/grafana` | No description |
| `alloy_brew_package` | str | `grafana/grafana/alloy` | No description |
| `alloy_service_plist` | str | `homebrew.mxcl.alloy` | No description |

## Tasks

### main.yml

- **Check if running on macOS** (ansible.builtin.assert)
- **Check if Homebrew is installed** (ansible.builtin.command)
- **Fail if Homebrew is not installed** (ansible.builtin.fail) - Conditional
- **Add Grafana tap to Homebrew** (community.general.homebrew_tap)
- **Install Alloy via Homebrew** (community.general.homebrew)
- **Get Homebrew prefix** (ansible.builtin.command)
- **Set Alloy config directory path** (ansible.builtin.set_fact)
- **Ensure Alloy config directory exists** (ansible.builtin.file)
- **Ensure ansible-logs directory exists** (ansible.builtin.file)
- **Deploy Alloy configuration** (ansible.builtin.template)
- **Check if Alloy service is loaded** (ansible.builtin.command)
- **Start and enable Alloy service** (ansible.builtin.command) - Conditional
- **Restart Alloy service if already running** (ansible.builtin.command) - Conditional
- **Stop Alloy service** (ansible.builtin.command) - Conditional
- **Verify Alloy installation** (ansible.builtin.command)
- **Display Alloy version** (ansible.builtin.debug) - Conditional
- **Wait for Alloy to start** (ansible.builtin.pause) - Conditional
- **Check Alloy service status** (ansible.builtin.command) - Conditional
- **Display Alloy service status** (ansible.builtin.debug) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - alloy
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms

- macOS: all
<!-- DOCSIBLE END -->
