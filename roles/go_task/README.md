# Ansible Role: go-task

This role installs and configures [go-task](https://github.com/go-task/task)
on Unix-like and Windows systems, providing a task runner for automation.

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
