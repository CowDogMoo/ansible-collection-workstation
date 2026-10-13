# Ansible Playbook: Workstation

This playbook sets up a complete development workstation with user management,
ZSH configuration, ASDF version manager, AI development tools (Fabric,
Claude Code, herdr, and firstmate), logging, and Go Task on Ubuntu, Debian, and macOS systems.

---

## Base Requirements

- Ansible 2.14 or higher.
- Python packages. Install with:

  ```bash
  python3 -m pip install --upgrade \
    ansible-core \
    molecule \
    molecule-docker \
    "molecule-plugins[docker]"
  ```

---

## Usage

### Basic Playbook Execution

```bash
ansible-playbook workstation.yml -i inventory
```

### Local Machine Setup

Host-specific settings live in `host_vars/<hostname>.yml` (or a
`host_vars/<hostname>/` directory) and only load when the inventory hostname
matches. Target your machine by its short hostname, from the repo root:

```bash
ansible-playbook playbooks/workstation/workstation.yml \
  -i "$(hostname -s)," -c local

# Limit the run to one role with its tag
ansible-playbook playbooks/workstation/workstation.yml \
  -i "$(hostname -s)," -c local --tags claude
```

Running without `-i` targets plain `localhost`, which matches no host_vars
file, so roles would fall back to their defaults and rewrite files such as
`~/.claude/settings.json` without the machine's settings. The playbook refuses
that: its first task fails when the target host has no host_vars entry and
prints the command to use instead. To run on role defaults deliberately (CI, a
fresh generic machine), pass `-e workstation_allow_missing_host_vars=true`.

### With specific hosts

```bash
ansible-playbook workstation.yml -i inventory --limit "dev-workstations"
```

---

## Testing

This playbook includes Molecule tests. To test the playbook:

```bash
# Run the full test sequence
molecule test

# Or run individual steps
molecule converge    # Deploy the playbook
molecule idempotence # Test idempotency
molecule verify      # Run verification tests
molecule destroy     # Clean up test instances
```

---

## Example Inventory

### Local Setup

Name the host after the machine's hostname so its host_vars load:

```ini
[all]
bringer-of-despair ansible_connection=local
```

### Remote Workstations

```ini
[dev_workstations]
dev1 ansible_host=192.168.1.50
dev2 ansible_host=192.168.1.51

[dev_workstations:vars]
ansible_user=ubuntu
ansible_become=yes
```

---

## Roles Included

This playbook includes the following roles in order:

1. **logging** - Sets up log directories and log rotation
1. **alloy** - Configures Grafana Alloy for log shipping to Loki
1. **user_setup** - Creates and configures system users
1. **zsh_setup** - Installs and configures ZSH with Oh-My-Zsh
1. **asdf** - Installs ASDF version manager and language runtimes
   (Go, Python, Ruby, etc.)
1. **fabric** - Installs Fabric AI framework via Go packages
1. **claude_code** - Installs and configures Claude Code CLI with hooks
1. **herdr** - Installs herdr and configures it and its agent integrations
1. **firstmate** - Clones the firstmate agent distro (no fleet setup or sessions)
1. **go_task** - Installs Go Task runner
