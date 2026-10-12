<!-- DOCSIBLE START -->
# herdr

## Description

Installs herdr, the terminal agent multiplexer, from Homebrew on macOS and pinned, checksum-verified release binaries elsewhere

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `herdr_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `herdr_usergroup` | str | <code>{{ (ansible_facts&#91;'user_gid'&#93; &#124; default('staff')) if ansible_facts&#91;'os_family'&#93; == 'Darwin' else herdr_username }}</code> | No description |
| `herdr_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `herdr_install_method` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('homebrew', 'binary') }}</code> | No description |
| `herdr_version` | str | <code>0.9.3</code> | No description |
| `herdr_install_dir` | str | <code><multiline value: folded_strip></code> | No description |
| `herdr_claude_integration` | bool | <code>True</code> | No description |
| `herdr_checksums` | dict | <code>{}</code> | No description |
| `herdr_arch_map` | dict | <code>{}</code> | No description |
| `herdr_arch_map.x86_64` | str | <code>x86_64</code> | No description |
| `herdr_arch_map.amd64` | str | <code>x86_64</code> | No description |
| `herdr_arch_map.aarch64` | str | <code>aarch64</code> | No description |
| `herdr_arch_map.arm64` | str | <code>aarch64</code> | No description |
| `herdr_os_map` | dict | <code>{}</code> | No description |
| `herdr_os_map.Linux` | str | <code>linux</code> | No description |
| `herdr_os_map.Darwin` | str | <code>macos</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| -------- | ---- | ----- | ----------- |
| `herdr_download_base_url` | str | `https://github.com/herdrdev/herdr/releases/download` | No description |

## Tasks

### claude-integration.yml


- **Check herdr Claude integration status** (ansible.builtin.command)
- **Install herdr Claude integration script** (block) - Conditional
- **Create herdr integration staging home** (ansible.builtin.tempfile)
- **Create Claude directory in the staging home** (ansible.builtin.file)
- **Generate herdr Claude integration in the staging home** (ansible.builtin.command)
- **Ensure Claude hooks directory exists** (ansible.builtin.file)
- **Copy herdr Claude integration script** (ansible.builtin.copy)

### install-binary.yml


- **Fail on unsupported platform** (ansible.builtin.fail) - Conditional
- **Set herdr release asset name** (ansible.builtin.set_fact)
- **Set herdr release checksum** (ansible.builtin.set_fact)
- **Fail when no checksum is known for the requested release** (ansible.builtin.fail) - Conditional
- **Check installed herdr binary** (ansible.builtin.stat)
- **Check installed herdr version** (ansible.builtin.command) - Conditional
- **Set herdr install escalation facts** (ansible.builtin.set_fact)
- **Ensure herdr install directory exists** (ansible.builtin.file)
- **Download herdr release binary** (ansible.builtin.get_url) - Conditional

### main.yml


- **Fail on unknown install method** (ansible.builtin.fail) - Conditional
- **Install herdr with Homebrew** (community.general.homebrew) - Conditional
- **Resolve Homebrew prefix** (ansible.builtin.command) - Conditional
- **Install herdr release binary** (ansible.builtin.include_tasks) - Conditional
- **Set herdr binary path** (ansible.builtin.set_fact)
- **Verify herdr installation** (ansible.builtin.command)
- **Display herdr version** (ansible.builtin.debug)
- **Install herdr Claude Code integration** (ansible.builtin.include_tasks) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - herdr
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
