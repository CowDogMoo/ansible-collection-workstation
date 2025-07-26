# Ansible Role: VNC Setup

This role configures VNC services with systemd integration, ensuring isolated
and secure remote desktop access for each user on Unix-like systems.

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

## Testing

This role includes Molecule tests. To test the role:

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

<!-- DOCSIBLE START -->
<!-- DOCSIBLE END -->
