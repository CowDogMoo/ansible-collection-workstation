# Ansible Role: Package Management

This role manages package installations and cleanups on Debian-based
and Red Hat-based systems.

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

## Role Variables

| Variable                                    | Default Value                                                                                                                                                     | Description                     |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| package_management_common_install_packages  | bash, ca-certificates, colordiff, dbus-x11, file, gcc, git, less, make, net-tools, procps, rsync, sudo, terminator, tree, wget, vim, zsh                          | Common packages for all systems |
| package_management_debian_specific_packages | curl, fonts-powerline, inetutils-ping, locales, software-properties-common, tigervnc-standalone-server, tigervnc-tools, xfce4-goodies, xfce4, zsh-autosuggestions | Debian-specific packages        |
| package_management_redhat_specific_packages | epel-release, tigervnc, tigervnc-server                                                                                                                           | Red Hat-specific packages       |

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
export PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.package_management"
```

## Testing

- Use [act](https://github.com/nektos/act) for local GitHub Actions testing.

- Run Molecule tests:

  ```bash
  molecule create
  molecule converge
  molecule idempotence
  molecule destroy
  ```

## Role Tasks

1. Include common variables.
2. Install distribution-specific packages.
3. Install common packages.
4. Cleanup unnecessary packages.
5. Configure .xinitrc for XFCE (Red Hat).
6. Manage systemd default target (Red Hat).

## Platforms

Tested on:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

No dependencies.

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
