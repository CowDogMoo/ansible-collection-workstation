<!-- DOCSIBLE START -->
# herdr

## Description

Installs and configures herdr, the terminal agent multiplexer, from Homebrew on macOS and pinned, checksum-verified release binaries elsewhere, with its agent integrations

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `herdr_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `herdr_usergroup` | str | <code>{{ (ansible_facts&#91;'user_gid'&#93; &#124; default('staff')) if ansible_facts&#91;'os_family'&#93; == 'Darwin' else herdr_username }}</code> | No description |
| `herdr_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `herdr_install` | bool | <code>True</code> | No description |
| `herdr_install_method` | str | <code>{{ (ansible_facts&#91;'os_family'&#93; == 'Darwin') &#124; ternary('homebrew', 'binary') }}</code> | No description |
| `herdr_version` | str | <code>0.9.3</code> | No description |
| `herdr_install_dir` | str | <code><multiline value: folded_strip></code> | No description |
| `herdr_binary_path` | str | <code></code> | No description |
| `herdr_integrations` | list | <code>&#91;&#93;</code> | No description |
| `herdr_integrations.0` | str | <code>claude</code> | No description |
| `herdr_integrations.1` | str | <code>antigravity-cli</code> | No description |
| `herdr_integrations.2` | str | <code>codex</code> | No description |
| `herdr_config_dir` | str | <code>{{ herdr_user_home }}/.config/herdr</code> | No description |
| `herdr_agent_detection_src_dir` | str | <code></code> | No description |
| `herdr_manage_config` | bool | <code>True</code> | No description |
| `herdr_backup_config` | bool | <code>True</code> | No description |
| `herdr_tmux_keybindings` | bool | <code>False</code> | No description |
| `herdr_manage_helpers` | bool | <code>False</code> | No description |
| `herdr_helper_dependencies` | list | <code>&#91;&#93;</code> | No description |
| `herdr_helper_dependencies.0` | str | <code>less</code> | No description |
| `herdr_helper_dependencies.1` | str | <code>python3</code> | No description |
| `herdr_create_herder_alias` | bool | <code>True</code> | No description |
| `herdr_onboarding` | bool | <code>False</code> | No description |
| `herdr_toast_delivery` | str | <code>off</code> | No description |
| `herdr_show_agent_labels_on_pane_borders` | bool | <code>False</code> | No description |
| `herdr_confirm_close` | bool | <code>True</code> | No description |
| `herdr_agent_panel_sort` | str | <code>spaces</code> | No description |
| `herdr_status_indicators` | str | <code>dots</code> | No description |
| `herdr_theme_name` | str | <code>catppuccin</code> | No description |
| `herdr_theme_auto_switch` | bool | <code>False</code> | No description |
| `herdr_prefix` | str | <code>ctrl+b</code> | No description |
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
| `herdr_config_upstream_defaults` | dict | `{}` | No description |
| `herdr_config_upstream_defaults.onboarding` | bool | `True` | No description |
| `herdr_config_upstream_defaults.toast_delivery` | str | `off` | No description |
| `herdr_config_upstream_defaults.show_agent_labels_on_pane_borders` | bool | `False` | No description |
| `herdr_config_upstream_defaults.confirm_close` | bool | `True` | No description |
| `herdr_config_upstream_defaults.agent_panel_sort` | str | `spaces` | No description |
| `herdr_config_upstream_defaults.status_indicators` | str | `dots` | No description |
| `herdr_config_upstream_defaults.theme_name` | str | `catppuccin` | No description |
| `herdr_config_upstream_defaults.theme_auto_switch` | bool | `False` | No description |
| `herdr_config_upstream_defaults.prefix` | str | `ctrl+b` | No description |
| `herdr_integration_specs` | dict | `{}` | No description |
| `herdr_integration_specs.claude` | dict | `{}` | No description |
| `herdr_integration_specs.claude.agent_dir` | str | `.claude` | No description |
| `herdr_integration_specs.claude.staged` | bool | `True` | No description |
| `herdr_integration_specs.claude.script` | str | `.claude/hooks/herdr-agent-state.sh` | No description |
| `herdr_integration_specs.antigravity-cli` | dict | `{}` | No description |
| `herdr_integration_specs.antigravity-cli.agent_dir` | str | `.gemini/config` | No description |
| `herdr_integration_specs.antigravity-cli.staged` | bool | `True` | No description |
| `herdr_integration_specs.antigravity-cli.script` | str | `.gemini/config/hooks/herdr-agent-state.sh` | No description |
| `herdr_integration_specs.codex` | dict | `{}` | No description |
| `herdr_integration_specs.codex.agent_dir` | str | `.codex` | No description |
| `herdr_integration_specs.codex.staged` | bool | `False` | No description |

## Tasks

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

### integrations.yml


- **Fail on unknown herdr integrations** (ansible.builtin.fail) - Conditional
- **Check herdr integration status** (ansible.builtin.command)
- **Check agent config directories** (ansible.builtin.stat)
- **Select herdr integrations to install** (ansible.builtin.set_fact)
- **Install staged herdr integration scripts** (block) - Conditional
- **Create herdr integration staging home** (ansible.builtin.tempfile)
- **Create agent config directories in the staging home** (ansible.builtin.file)
- **Generate herdr integrations in the staging home** (ansible.builtin.command)
- **Ensure agent hook directories exist** (ansible.builtin.file)
- **Copy herdr integration scripts** (ansible.builtin.copy)
- **Install herdr integrations in place** (ansible.builtin.command) - Conditional

### main.yml


- **Fail on unknown install method** (ansible.builtin.fail) - Conditional
- **Install herdr with Homebrew** (community.general.homebrew) - Conditional
- **Resolve Homebrew prefix** (ansible.builtin.command) - Conditional
- **Install herdr release binary** (ansible.builtin.include_tasks) - Conditional
- **Find an existing herdr binary** (ansible.builtin.shell) - Conditional
- **Set herdr binary path** (ansible.builtin.set_fact)
- **Check herdr binary** (ansible.builtin.stat)
- **Verify herdr installation** (ansible.builtin.command) - Conditional
- **Display herdr version** (ansible.builtin.debug) - Conditional
- **Report missing herdr binary** (ansible.builtin.debug) - Conditional
- **Ensure herder alias directory exists** (ansible.builtin.file) - Conditional
- **Create herder symlink to herdr** (ansible.builtin.file) - Conditional
- **Ensure herdr configuration directory exists** (ansible.builtin.file) - Conditional
- **Install herdr helper script dependencies** (ansible.builtin.package) - Conditional
- **Deploy herdr helper scripts** (ansible.builtin.copy) - Conditional
- **Ensure herdr agent-detection directory exists** (ansible.builtin.file) - Conditional
- **Install custom herdr agent-detection overrides** (ansible.builtin.copy) - Conditional
- **Render herdr config.toml** (ansible.builtin.template) - Conditional
- **Install herdr agent integrations** (ansible.builtin.include_tasks) - Conditional

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
