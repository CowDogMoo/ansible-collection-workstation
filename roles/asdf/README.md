# Ansible Role: asdf

This role installs and configures the `asdf` version manager for multiple
programming languages on Unix-like systems.

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
