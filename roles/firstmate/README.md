<!-- DOCSIBLE START -->
# firstmate

## Description

Installs the firstmate agent distro by cloning its repository and installs its dispatch gate, without starting sessions

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `firstmate_username` | str | <code>{{ ansible_facts&#91;'user_id'&#93; &#124; default(ansible_facts&#91;'user'&#93;) }}</code> | User who owns the firstmate checkout. |
| `firstmate_user_home` | str | <code><multiline value: folded_strip></code> | Home directory of firstmate_username. |
| `firstmate_repo_url` | str | <code>https://github.com/kunchenguid/firstmate.git</code> | Git repository firstmate is cloned from. |
| `firstmate_version` | str | <code>main</code> | Branch, tag, or commit checked out on the initial clone. |
| `firstmate_install_dir` | str | <code>{{ firstmate_user_home }}/firstmate</code> | Where the firstmate checkout lives. |
| `firstmate_update` | bool | <code>False</code> | Fetch and check out firstmate_version on an existing checkout. |
| `firstmate_manage_dependencies` | bool | <code>True</code> | Install firstmate_dependencies with the system package manager (Linux only). |
| `firstmate_dependencies` | list | <code>&#91;&#93;</code> | Packages installed when firstmate_manage_dependencies is true. |
| `firstmate_dependencies.0` | str | <code>git</code> | No description |
| `firstmate_dependencies.1` | str | <code>jq</code> | No description |
| `firstmate_ship_harnesses` | list | <code>&#91;&#93;</code> | Harnesses allowed to run ship tasks, rendered to config/ship-harnesses. |
| `firstmate_ship_harnesses.0` | str | <code>claude</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| -------- | ---- | ----- | ----------- |
| `firstmate_dispatch_gate_hook` | dict | `{}` | No description |
| `firstmate_dispatch_gate_hook.matcher` | str | `Bash` | No description |
| `firstmate_dispatch_gate_hook.hooks` | list | `[]` | No description |
| `firstmate_dispatch_gate_hook.hooks.0` | dict | `{}` | No description |
| `firstmate_dispatch_gate_hook.hooks.0.type` | str | `command` | No description |
| `firstmate_dispatch_gate_hook.hooks.0.command` | str | `/usr/bin/python3 "$CLAUDE_PROJECT_DIR"/config/hooks/fm-dispatch-gate.py` | No description |
| `firstmate_dispatch_gate_hook.hooks.0.timeout` | int | `10` | No description |

## Tasks

### dispatch-gate.yml


- **Check the firstmate checkout before configuring it** (ansible.builtin.stat)
- **Report the dispatch gate as skipped without a checkout** (ansible.builtin.debug) - Conditional
- **Install the dispatch gate** (block) - Conditional
- **Check for an existing .claude/settings.local.json** (ansible.builtin.stat)
- **Read the existing .claude/settings.local.json** (ansible.builtin.slurp) - Conditional
- **Parse .claude/settings.local.json** (ansible.builtin.set_fact)
- **Assert .claude/settings.local.json holds a JSON object** (ansible.builtin.assert)
- **Decide whether the dispatch gate hook entry is missing** (ansible.builtin.set_fact)
- **Check the paths are gitignored by the checkout** (ansible.builtin.command)
- **Refuse to write paths the checkout does not ignore** (ansible.builtin.assert)
- **Check the settings backup path is gitignored** (ansible.builtin.command) - Conditional
- **Locate the checkout's local exclude file** (ansible.builtin.command) - Conditional
- **Ignore .claude/settings.local.json backups locally** (ansible.builtin.lineinfile) - Conditional
- **Create the config directories** (ansible.builtin.file)
- **Install config/crew-dispatch.json** (ansible.builtin.copy)
- **Render config/ship-harnesses** (ansible.builtin.template)
- **Install the dispatch gate hook and its test** (ansible.builtin.copy)
- **Merge the dispatch gate hook into .claude/settings.local.json** (ansible.builtin.copy) - Conditional

### main.yml


- **Install firstmate dependencies** (ansible.builtin.package) - Conditional
- **Check for an existing firstmate checkout** (ansible.builtin.stat)
- **Clone firstmate** (ansible.builtin.git) - Conditional
- **Display firstmate checkout** (ansible.builtin.debug)
- **Install the firstmate dispatch gate** (ansible.builtin.include_tasks)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - firstmate
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
