# Ansible Playbook: Workstation

This playbook sets up a complete development workstation with user management,
ZSH configuration, ASDF version manager, and Go Task on Ubuntu systems.

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
