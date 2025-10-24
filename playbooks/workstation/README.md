# Ansible Playbook: Workstation

This playbook sets up a complete development workstation with user management,
ZSH configuration, ASDF version manager, AI development tools (Fabric and
Claude Code), logging, and Go Task on Ubuntu, Debian, and macOS systems.

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

For setting up your local machine:

```bash
ansible-playbook workstation.yml -i inventory --connection=local
```

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

```ini
[all]
localhost ansible_connection=local
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
1. **go_task** - Installs Go Task runner
