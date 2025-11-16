<!-- DOCSIBLE START -->
# asdf

## Description

Install asdf

## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.package_management

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `asdf_username` | str | `{{ ansible_facts['user_id'] \| default(ansible_facts['user']) }}` | No description |
| `asdf_usergroup` | str | `{{ (ansible_facts['os_family'] == 'Darwin') \| ternary('staff', asdf_username) }}` | No description |
| `asdf_user_home` | str | `<multiline value: folded_strip>` | No description |
| `asdf_bin_dir` | str | `{{ (ansible_facts['os_family'] == 'Darwin') \| ternary('/usr/local/bin', '/usr/local/bin') }}` | No description |
| `asdf_data_dir` | str | `{{ asdf_user_home }}/.asdf` | No description |
| `asdf_shells` | list | `[]` | No description |
| `asdf_shells.0` | str | `/usr/bin/zsh` | No description |
| `asdf_shells.1` | str | `/bin/zsh` | No description |
| `asdf_shells.2` | str | `/usr/bin/bash` | No description |
| `asdf_shells.3` | str | `/bin/bash` | No description |
| `asdf_shell` | str | `{{ '/bin/zsh' if ansible_facts['distribution'] == 'MacOSX' else '/bin/bash' }}` | No description |
| `asdf_plugins` | list | `[]` | No description |
| `asdf_plugins.0` | dict | `{}` | No description |
| `asdf_plugins.1` | dict | `{}` | No description |
| `asdf_plugins.2` | dict | `{}` | No description |
| `asdf_plugins.3` | dict | `{}` | No description |
| `asdf_plugins.4` | dict | `{}` | No description |
| `asdf_plugins.5` | dict | `{}` | No description |
| `asdf_plugins.6` | dict | `{}` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `asdf_version` | str | `0.18.0` | No description |
| `asdf_arch` | str | `{{ 'arm64' if ansible_facts['architecture'] in ['aarch64', 'arm64'] else 'amd64' if ansible_facts['architecture'] == 'x86_64' else '386' }}` | No description |
| `asdf_os` | str | `{{ 'darwin' if ansible_facts['system'] == 'Darwin' else 'linux' }}` | No description |
| `asdf_download_url` | str | `https://github.com/asdf-vm/asdf/releases/download/v{{ asdf_version }}/asdf-v{{ asdf_version }}-{{ asdf_os }}-{{ asdf_arch }}.tar.gz` | No description |
| `asdf_checksum_url` | str | `{{ asdf_download_url }}.md5` | No description |

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
- **Reapply external asdf_plugins variable if provided** (ansible.builtin.set_fact) - Conditional
- **Check available shells** (ansible.builtin.stat)
- **Set available shell fact** (ansible.builtin.set_fact)
- **Create bin directory if it doesn't exist** (ansible.builtin.file)
- **Fetch and install ASDF binary** (block)
- **Check if checksum file exists** (ansible.builtin.stat)
- **Fetch ASDF MD5 checksum** (ansible.builtin.get_url) - Conditional
- **Extract ASDF MD5 checksum** (ansible.builtin.command)
- **Download ASDF binary** (ansible.builtin.get_url)
- **Extract ASDF binary** (ansible.builtin.unarchive)
- **Setup ASDF data directory structure** (ansible.builtin.file)
- **Setup ASDF shims directory** (ansible.builtin.file)
- **Update shell profile** (ansible.builtin.include_tasks)
- **Install libyaml from source** (ansible.builtin.include_tasks) - Conditional
- **Set common ASDF environment variables** (ansible.builtin.set_fact)
- **Verify ASDF installation** (ansible.builtin.shell)
- **Generate ASDF plugin installation script** (ansible.builtin.template)
- **Install ASDF plugins** (ansible.builtin.shell)
- **Generate .tool-versions file** (ansible.builtin.template)
- **Reshim after default packages** (ansible.builtin.shell)

### update_shell_profile.yml

- **Detect shell and set profile** (block)
- **Check if shell exists** (ansible.builtin.command)
- **Set detected shell fact** (ansible.builtin.set_fact)
- **Update shell profile for the user** (ansible.builtin.blockinfile)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - asdf
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
