# Ansible Playbook: VNC Box

This playbook sets up a complete VNC-enabled workstation with user management,
ZSH configuration, and VNC server on Ubuntu and Kali Linux systems.

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
ansible-playbook vnc_box.yml -i inventory
```

### With specific hosts

```bash
ansible-playbook vnc_box.yml -i inventory --limit "ubuntu-servers"
```

---

## Testing

This playbook includes Molecule tests for both Ubuntu and Kali Linux platforms.
To test the playbook:

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

```ini
[vnc_workstations]
workstation1 ansible_host=192.168.1.100
workstation2 ansible_host=192.168.1.101

[vnc_workstations:vars]
ansible_user=ubuntu
ansible_become=true
```

---

<!-- DOCSIBLE START -->
<!-- DOCSIBLE END -->
