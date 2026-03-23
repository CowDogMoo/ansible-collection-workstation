<!-- DOCSIBLE START -->
# mise

## Description

Install mise

## Requirements

- Ansible >= 2.14

## Dependencies


- cowdogmoo.workstation.package_management

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `mise_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `mise_usergroup` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('staff', mise_username) }}</code> | No description |
| `mise_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `mise_bin_dir` | str | <code>/usr/local/bin</code> | No description |
| `mise_data_dir` | str | <code>{{ mise_user_home }}/.local/share/mise</code> | No description |
| `mise_config_dir` | str | <code>{{ mise_user_home }}/.config/mise</code> | No description |
| `mise_shells` | list | <code>&#91;&#93;</code> | No description |
| `mise_shells.0` | str | <code>/usr/bin/zsh</code> | No description |
| `mise_shells.1` | str | <code>/bin/zsh</code> | No description |
| `mise_shells.2` | str | <code>/usr/bin/bash</code> | No description |
| `mise_shells.3` | str | <code>/bin/bash</code> | No description |
| `mise_shell` | str | <code>{{ '/bin/zsh' if ansible_facts&#91;'distribution'&#93; == 'MacOSX' else '/bin/bash' }}</code> | No description |
| `mise_plugins` | list | <code>&#91;&#93;</code> | No description |
| `mise_plugins.0` | dict | <code>{}</code> | No description |
| `mise_plugins.1` | dict | <code>{}</code> | No description |
| `mise_plugins.2` | dict | <code>{}</code> | No description |
| `mise_plugins.3` | dict | <code>{}</code> | No description |
| `mise_plugins.4` | dict | <code>{}</code> | No description |
| `mise_plugins.5` | dict | <code>{}</code> | No description |
| `mise_plugins.6` | dict | <code>{}</code> | No description |
| `mise_plugins.7` | dict | <code>{}</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| -------- | ---- | ----- | ----------- |
| `mise_version` | str | `2026.3.12` | No description |
| `mise_arch` | str | `{{ 'arm64' if ansible_facts['architecture'] in ['aarch64', 'arm64'] else 'x64' }}` | No description |
| `mise_os` | str | `{{ 'macos' if ansible_facts['system'] == 'Darwin' else 'linux' }}` | No description |
| `mise_download_url` | str | `https://github.com/jdx/mise/releases/download/v{{ mise_version }}/mise-v{{ mise_version }}-{{ mise_os }}-{{ mise_arch }}.tar.gz` | No description |
| `mise_checksum_url` | str | `https://github.com/jdx/mise/releases/download/v{{ mise_version }}/SHASUMS256.txt` | No description |

## Tasks

### ensure_directory_exists.yml


- **Ensure directory exists** (ansible.builtin.file)

### install_libyaml.yml


- **Check if libyaml is installed** (ansible.builtin.command)
- **Download, extract, compile, and install libyaml** (block) - Conditional
- **Download libyaml source** (ansible.builtin.get_url)
- **Extract libyaml tarball** (ansible.builtin.unarchive)
- **Compile and install libyaml** (ansible.builtin.shell)

### main.yml


- **Set default username for Kali systems** (ansible.builtin.set_fact) - Conditional
- **Reapply external mise_plugins variable if provided** (ansible.builtin.set_fact) - Conditional
- **Check available shells** (ansible.builtin.stat)
- **Set available shell fact** (ansible.builtin.set_fact)
- **Create bin directory if it doesn't exist** (ansible.builtin.file)
- **Check if mise is already installed** (ansible.builtin.stat)
- **Check installed mise version** (ansible.builtin.command) - Conditional
- **Fetch and install mise binary** (block) - Conditional
- **Download mise archive** (ansible.builtin.get_url)
- **Create temporary extraction directory** (ansible.builtin.file)
- **Extract mise archive** (ansible.builtin.unarchive)
- **Find mise binary in extracted archive** (ansible.builtin.find)
- **Install mise binary** (ansible.builtin.copy)
- **Clean up extraction directory** (ansible.builtin.file)
- **Setup mise data directory** (ansible.builtin.file)
- **Setup mise config directory** (ansible.builtin.file)
- **Setup mise shims directory** (ansible.builtin.file)
- **Update shell profile** (ansible.builtin.include_tasks)
- **Install libyaml from source** (ansible.builtin.include_tasks) - Conditional
- **Set common mise environment variables** (ansible.builtin.set_fact)
- **Verify mise installation** (ansible.builtin.shell)
- **Generate mise plugin installation script** (ansible.builtin.template)
- **Install mise plugins** (ansible.builtin.shell)
- **Generate mise config file** (ansible.builtin.template)
- **Reshim after installations** (ansible.builtin.shell)

### update_shell_profile.yml


- **Detect shell and set profile** (block)
- **Check if shell exists** (ansible.builtin.command)
- **Set detected shell fact** (ansible.builtin.set_fact)
- **Update shell profile for the user** (ansible.builtin.blockinfile)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - mise
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: all
- macOS: all
- EL: all
<!-- DOCSIBLE END -->
