# Ansible Role: Package Management

This role manages package installations and cleanups on Debian and Red
Hat-based systems.

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

| Variable                                    | Default Value                                        |
| ------------------------------------------- | ---------------------------------------------------- |
| package_management_common_install_packages  | autoconf, bash, bison, ... (list of common packages) |
| package_management_install_packages         | Conditional selection based on OS family             |
| package_management_debian_specific_packages | build-essential, curl, fonts-powerline, ...          |
| package_management_redhat_specific_packages | bzip2-devel, epel-release, gcc, gcc-c++, ...         |

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

- Include common variables.
- Install distribution-specific packages.
- Install common packages.
- Configure .xinitrc for XFCE (Red Hat).
- Check and set systemd default target (Red Hat).

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

No dependencies.

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
