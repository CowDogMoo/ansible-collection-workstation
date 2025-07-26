<!-- DOCSIBLE START -->
# vnc_setup

## Description

Provides logging directories and log rotation for other roles.

## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.user_setup

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `vnc_setup_client_options` | str | `-geometry 1920x1080` | No description |
| `vnc_setup_depth` | str | `24` | No description |
| `vnc_setup_systemd` | bool | `True` | No description |
| `vnc_setup_users` | list | `[]` | No description |
| `vnc_setup_users.0` | dict | `{}` | No description |
| `vnc_setup_default_username` | str | `{{ ansible_distribution | lower }}` | No description |
| `vnc_setup_vncpwd_clone_path` | str | `/tmp/vncpwd` | No description |
| `vnc_setup_vncpwd_path` | str | `/usr/local/bin/vncpwd` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `vnc_setup_common_install_packages` | list | `[]` | No description |
| `vnc_setup_common_install_packages.0` | str | `dbus-x11` | No description |
| `vnc_setup_debian_specific_packages` | list | `[]` | No description |
| `vnc_setup_debian_specific_packages.0` | str | `tigervnc-standalone-server` | No description |
| `vnc_setup_debian_specific_packages.1` | str | `tigervnc-tools` | No description |
| `vnc_setup_debian_specific_packages.2` | str | `xfce4-goodies` | No description |
| `vnc_setup_debian_specific_packages.3` | str | `xfce4` | No description |
| `vnc_setup_redhat_specific_packages` | list | `[]` | No description |
| `vnc_setup_redhat_specific_packages.0` | str | `tigervnc` | No description |
| `vnc_setup_redhat_specific_packages.1` | str | `tigervnc-server` | No description |
| `vnc_setup_vncpwd_repo_url` | str | `https://github.com/jeroennijhof/vncpwd.git` | No description |

## Tasks

### cleanup.yml

- **Check if VNC needs to be restarted** (ansible.builtin.set_fact)
- **Attempt to stop VNC using vncserver -kill** (ansible.builtin.shell) - Conditional
- **Get running VNC processes for users** (ansible.builtin.command) - Conditional
- **Stop VNC processes with SIGTERM first** (ansible.builtin.shell) - Conditional
- **Wait for processes to terminate gracefully** (ansible.builtin.pause) - Conditional
- **Force kill remaining VNC processes with SIGKILL** (ansible.builtin.shell) - Conditional
- **Clean up VNC lock files** (ansible.builtin.file) - Conditional
- **Clean up VNC socket files** (ansible.builtin.file) - Conditional
- **Clean up VNC PID files** (ansible.builtin.shell) - Conditional

### get_uids.yml

- **Get uids of users** (ansible.builtin.command) - Conditional
- **Create uid_results from uids** (ansible.builtin.set_fact) - Conditional
- **Merge uids into vnc_setup_users** (cowdogmoo.workstation.merge_list_dicts_into_list) - Conditional

### main.yml

- **Install vncpwd** (ansible.builtin.import_tasks)
- **Install required packages for vnc** (ansible.builtin.include_role)
- **Set OS-specific defaults** (ansible.builtin.set_fact)
- **Configure shell environments** (ansible.builtin.import_tasks)
- **Prepare user VNC directories and configurations** (ansible.builtin.import_tasks)
- **Generate and set VNC passwords** (ansible.builtin.import_tasks)
- **Determine if systemd is present** (ansible.builtin.command)
- **Set fact for systemd presence** (ansible.builtin.set_fact)
- **Get user UIDs** (ansible.builtin.import_tasks)
- **Configure systemd for VNC** (ansible.builtin.import_tasks) - Conditional
- **Start VNC services (non-systemd or systemd startup failure recovery)** (ansible.builtin.import_tasks)

### password_config.yml

- **Generate random passwords for vnc_setup_users with vnc_pw.py** (cowdogmoo.workstation.vnc_pw)
- **Update vnc_setup_users with the random generated passwords** (ansible.builtin.set_fact)
- **Process VNC passwords** (block)
- **Check if VNC password file exists** (ansible.builtin.stat)
- **Generate and set VNC passwords** (ansible.builtin.shell) - Conditional
- **Set permissions on VNC password files** (ansible.builtin.file)

### service.yml

- **Clean up existing VNC sessions** (ansible.builtin.import_tasks) - Conditional
- **Start VNC directly when systemd failed or is unavailable** (block) - Conditional
- **Check if VNC is already running for each user (broader check)** (ansible.builtin.shell)
- **Set fact for when VNC needs to be restarted** (ansible.builtin.set_fact)
- **Start VNC service directly for each user** (ansible.builtin.shell) - Conditional

### shell_config.yml

- **Check if zshrc file exists** (ansible.builtin.stat)
- **Ensure zsh sources /etc/profile.d scripts** (ansible.builtin.lineinfile)
- **Create docker-entrypoint.sh** (ansible.builtin.template)

### systemd.yml

- **Clean up existing VNC sessions** (ansible.builtin.import_tasks)
- **Ensure required systemd services are running** (ansible.builtin.service)
- **Configure user runtime directories** (block)
- **Create tmpfiles.d configuration** (ansible.builtin.copy)
- **Apply tmpfiles configuration** (ansible.builtin.command)
- **Ensure user runtime directories exist** (ansible.builtin.file)
- **Create XDG_RUNTIME_DIR script in /etc/profile.d** (ansible.builtin.copy)
- **Ensure dconf directory exists in runtime dir** (ansible.builtin.file)
- **Configure systemd services for VNC** (block)
- **Enable persistent services for all users** (ansible.builtin.command)
- **Create systemd directories** (ansible.builtin.file)
- **Update per-user systemd service files** (ansible.builtin.template) - Conditional
- **Add start_vnc script to profile.d** (ansible.builtin.template)
- **Check VNC service status** (ansible.builtin.command)
- **Stop VNC service if running and configs changed** (ansible.builtin.systemd) - Conditional
- **Start VNC service with systemd** (block)
- **Start VNC service with systemd** (ansible.builtin.systemd) - Conditional
- **Check if VNC started successfully with systemd** (ansible.builtin.command)
- **Set fact for systemd start success** (ansible.builtin.set_fact) - Conditional

### user_config.yml

- **Create .vnc directories for all users** (ansible.builtin.file)
- **Create xstartup file for VNC** (ansible.builtin.template)

### vncpwd.yml

- **Clone repo** (ansible.builtin.git)
- **Build vncpwd** (community.general.make)
- **Move vncpwd into $PATH** (ansible.builtin.copy)
- **Clean up** (ansible.builtin.file)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - vnc_setup
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
