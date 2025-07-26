# Ansible Role: User Setup

This role sets up user accounts with optional sudo privileges for Unix-like
systems.

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

To test the role, use Molecule:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

---

<!-- DOCSIBLE START -->

<!-- DOCSIBLE END -->
