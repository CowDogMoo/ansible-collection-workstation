# Ansible Role: Package Management

This role manages package installations and cleanups on Debian and Red
Hat-based systems.

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
