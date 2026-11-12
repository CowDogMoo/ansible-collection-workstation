<!-- DOCSIBLE START -->
# codex

## Description

Installs the Codex CLI and manages its global AGENTS.md, execpolicy rules, and hooks

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `codex_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | No description |
| `codex_usergroup` | str | <code>{{ (ansible_facts&#91;'user_gid'&#93; &#124; default('staff')) if ansible_facts&#91;'os_family'&#93; == 'Darwin' else codex_username }}</code> | No description |
| `codex_user_home` | str | <code><multiline value: folded_strip></code> | No description |
| `codex_home` | str | <code>{{ codex_user_home }}/.codex</code> | No description |
| `codex_homebrew_prefix` | str | <code><multiline value: folded_strip></code> | No description |
| `codex_path` | str | <code>{{ codex_homebrew_prefix }}/bin:{{ codex_user_home }}/.local/bin:/usr/local/bin:/usr/bin:/bin</code> | No description |
| `codex_install` | bool | <code>True</code> | No description |
| `codex_homebrew_cask` | str | <code>codex</code> | No description |
| `codex_npm_package` | str | <code>@openai/codex</code> | No description |
| `codex_npm_version` | str | <code></code> | No description |
| `codex_npm_become` | bool | <code>True</code> | No description |
| `codex_agents_md_file` | str | <code>{{ codex_home }}/AGENTS.md</code> | No description |
| `codex_agents_md_src` | str | <code>AGENTS.md</code> | No description |
| `codex_agents_md_content` | str | <code></code> | No description |
| `codex_manage_instructions` | bool | <code>True</code> | No description |
| `codex_manage_rules` | bool | <code>True</code> | No description |
| `codex_rules_dir` | str | <code>{{ codex_home }}/rules</code> | No description |
| `codex_bundled_rules` | list | <code>&#91;&#93;</code> | No description |
| `codex_bundled_rules.0` | str | <code>squad-only.rules</code> | No description |
| `codex_rules_extra` | list | <code>&#91;&#93;</code> | No description |
| `codex_validate_rules` | bool | <code>True</code> | No description |
| `codex_rules_probes` | list | <code>&#91;&#93;</code> | No description |
| `codex_rules_probes.0` | dict | <code>{}</code> | No description |
| `codex_rules_probes.1` | dict | <code>{}</code> | No description |
| `codex_rules_probes.2` | dict | <code>{}</code> | No description |
| `codex_rules_probes.3` | dict | <code>{}</code> | No description |
| `codex_rules_probes.4` | dict | <code>{}</code> | No description |
| `codex_rules_probes.5` | dict | <code>{}</code> | No description |
| `codex_manage_hooks` | bool | <code>False</code> | No description |
| `codex_hooks_file` | str | <code>{{ codex_home }}/hooks.json</code> | No description |
| `codex_hooks_marker` | str | <code># managed by cowdogmoo.workstation.codex:</code> | No description |
| `codex_hooks_default` | dict | <code>{}</code> | No description |
| `codex_hooks_default.forbidden_content` | dict | <code>{}</code> | No description |
| `codex_hooks_overrides` | dict | <code>{}</code> | No description |
| `codex_hooks` | str | <code><multiline value: folded_strip></code> | No description |

## Tasks

### hooks.yml


- **Check for an existing hooks.json** (ansible.builtin.stat)
- **Read the existing hooks.json** (ansible.builtin.slurp) - Conditional
- **Parse the existing hooks.json** (ansible.builtin.set_fact)
- **Merge the managed hooks into hooks.json** (ansible.builtin.template)

### install-linux.yml


- **Check if codex is already installed** (ansible.builtin.command)
- **Check for npm** (ansible.builtin.command) - Conditional
- **Install Codex from npm** (community.general.npm) - Conditional
- **Print manual install notice** (ansible.builtin.debug) - Conditional
- **Read the codex version** (ansible.builtin.command)
- **Display the codex version** (ansible.builtin.debug) - Conditional

### install-macos.yml


- **Check if codex is already installed** (ansible.builtin.command)
- **Install the Codex cask** (community.general.homebrew_cask) - Conditional
- **Read the codex version** (ansible.builtin.command)
- **Display the codex version** (ansible.builtin.debug) - Conditional

### main.yml


- **Check the codex user home directory** (ansible.builtin.stat)
- **Fail if the user home directory doesn't exist** (ansible.builtin.fail) - Conditional
- **Install Codex on macOS** (ansible.builtin.include_tasks) - Conditional
- **Install Codex on Linux** (ansible.builtin.include_tasks) - Conditional
- **Create the Codex home directory** (ansible.builtin.file)
- **Install the global AGENTS.md** (ansible.builtin.copy) - Conditional
- **Install execpolicy rules** (ansible.builtin.include_tasks) - Conditional
- **Merge hooks into hooks.json** (ansible.builtin.include_tasks) - Conditional
- **Display configuration status** (ansible.builtin.debug)

### rules.yml


- **Create the Codex rules directory** (ansible.builtin.file)
- **Install bundled rule files** (ansible.builtin.copy)
- **Install extra rule files** (ansible.builtin.copy)
- **Refuse a managed rule file named default.rules** (ansible.builtin.assert)
- **Validate the installed rules with codex** (ansible.builtin.include_tasks) - Conditional

### validate-rules.yml


- **Look for the codex binary** (ansible.builtin.command)
- **Report that rule validation was skipped** (ansible.builtin.debug) - Conditional
- **Check the installed rules with codex execpolicy** (block) - Conditional
- **Find the rule files Codex loads** (ansible.builtin.find)
- **Evaluate each probe against the installed rules** (ansible.builtin.command)
- **Assert each probe got the expected decision** (ansible.builtin.assert)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - codex
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: focal, jammy
- Debian: bullseye, bookworm
- EL: 8, 9
- MacOSX: all
<!-- DOCSIBLE END -->
