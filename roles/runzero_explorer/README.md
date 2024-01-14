# Ansible Role: RunZero Explorer

This role installs and executes the
[runZero Explorer](https://console.runzero.com/deploy/download/explorers)
on Debian, Red Hat, and Windows-based systems.

---

## Requirements

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

## Role Variables

No role-specific variables are defined. The role uses `ansible_os_family` to
determine the appropriate actions based on the operating system.

---

## Testing

To test the role, use Molecule:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

## Role Tasks

Key tasks in this role:

- Determine the download URL for runZero Explorer based on the OS family.
- Download the runZero Explorer binary or executable.
- Execute the runZero Explorer.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Debian
- Kali
- EL (Enterprise Linux)
- Windows

## Author Information

This role was created by Jayson Grace and is maintained as part of the
CowDogMoo project.
