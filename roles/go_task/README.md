<!-- DOCSIBLE START -->
# go_task

## Description

Installs go-task (Task runner) on Unix-like and Windows systems

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `go_task_version` | str | `latest` | No description |
| `go_task_install_dir` | str | `/usr/local/bin` | No description |
| `go_task_windows_install_dir` | str | `C:\\Program Files\\task` | No description |
| `go_task_windows_add_to_path` | bool | `True` | No description |
| `go_task_github_token` | str | `{{ lookup('env', 'GITHUB_TOKEN') \| default('') }}` | No description |
| `go_task_arch_map` | dict | `{}` | No description |
| `go_task_arch_map.x86_64` | str | `amd64` | No description |
| `go_task_arch_map.aarch64` | str | `arm64` | No description |
| `go_task_arch_map.armv7l` | str | `arm` | No description |
| `go_task_arch_map.i386` | int | `386` | No description |
| `go_task_arch_map.i686` | int | `386` | No description |
| `go_task_os_map` | dict | `{}` | No description |
| `go_task_os_map.Linux` | str | `linux` | No description |
| `go_task_os_map.Darwin` | str | `darwin` | No description |
| `go_task_os_map.Windows` | str | `windows` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `go_task_github_api_url` | str | `https://api.github.com/repos/go-task/task/releases` | No description |
| `go_task_download_base_url` | str | `https://github.com/go-task/task/releases/download` | No description |
| `go_task_checksums_file` | str | `task_checksums.txt` | No description |

## Tasks

### install-unix.yml

- **Set download filename for Unix-like systems** (ansible.builtin.set_fact)
- **Check if go-task is already installed** (ansible.builtin.stat)
- **Check installed go-task version** (ansible.builtin.command) - Conditional
- **Set fact for whether installation is needed** (ansible.builtin.set_fact)
- **Download and install go-task** (block) - Conditional
- **Create temporary download directory** (ansible.builtin.tempfile)
- **Download checksums file** (ansible.builtin.get_url)
- **Extract checksum for specific file** (ansible.builtin.shell)
- **Download go-task archive** (ansible.builtin.get_url)
- **Extract go-task archive** (ansible.builtin.unarchive)
- **Ensure installation directory exists** (ansible.builtin.file) - Conditional
- **Install go-task binary** (ansible.builtin.copy)

### install-windows.yml

- **Set download filename for Windows** (ansible.builtin.set_fact)
- **Create installation directory** (ansible.windows.win_file)
- **Download go-task for Windows** (ansible.windows.win_get_url)
- **Extract go-task archive** (community.windows.win_unzip)
- **Remove downloaded archive** (ansible.windows.win_file)
- **Add go-task to PATH** (ansible.windows.win_path) - Conditional

### main.yml

- **Include OS-specific variables** (ansible.builtin.include_vars)
- **Determine system architecture** (ansible.builtin.set_fact)
- **Determine system OS** (ansible.builtin.set_fact)
- **Check if go-task is already installed** (ansible.builtin.stat) - Conditional
- **Check if go-task is already installed on Windows** (ansible.windows.win_stat) - Conditional
- **Get installed version** (ansible.builtin.command) - Conditional
- **Get installed version on Windows** (ansible.windows.win_command) - Conditional
- **Get latest version if not specified** (block) - Conditional
- **Get latest release information** (ansible.builtin.uri)
- **Set version to latest** (ansible.builtin.set_fact)
- **Determine if installation is needed** (ansible.builtin.set_fact)
- **Install go-task on Unix-like systems** (ansible.builtin.include_tasks) - Conditional
- **Install go-task on Windows systems** (ansible.builtin.include_tasks) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - go_task
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
- Windows: all
<!-- DOCSIBLE END -->
