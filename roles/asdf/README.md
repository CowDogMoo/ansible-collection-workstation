# Ansible Role: ASDF

This role installs and configures the ASDF version manager for managing
multiple language runtime versions on Unix-like systems.

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

| Variable              | Default Value                         | Description                                                 |
| --------------------- | ------------------------------------- | ----------------------------------------------------------- |
| asdf_git_repo         | "https://github.com/asdf-vm/asdf.git" | Git repository URL for ASDF.                                |
| asdf_languages        | Configurable                          | Languages to configure with ASDF.                           |
| asdf_os_family        | "{{ ansible_os_family \| lower }}"    | OS family for loading specific tasks.                       |
| asdf_install_packages | Varies based on OS                    | Packages to be installed, listed in OS-specific vars files. |
| asdf_default_username | "{{ ansible_distribution \| lower }}" | Default username, typically the distribution name.          |
| asdf_users            | Configurable                          | List of users to set up with ASDF.                          |

### OS-Specific Variables

- `./vars/redhat.yml` for Red Hat-based systems.
- `./vars/debian.yml` for Debian-based systems.

---

## Local Development

To develop locally:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.asdf"
```

## Testing

For local testing:

- Use [act](https://github.com/nektos/act) for local GitHub Actions testing.

- Run Molecule tests:

  ```bash
  ACTION="molecule"
  if [[ $(uname) == "Darwin" ]]; then
    act -j $ACTION --container-architecture linux/amd64
  fi
  ```

To test changes made to this role locally:

```bash
molecule create
molecule converge
molecule idempotence
molecule destroy
```

## Role Tasks

The role includes the following main tasks:

1. Install necessary packages based on the operating system.
2. Clone the ASDF repository.
3. Check and download necessary scripts for each user.
4. Ensure .bashrc or .zshrc exists and is configured correctly.
5. Update shell profiles with ASDF settings.
6. Reload shell to apply ASDF settings.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

- `cowdogmoo.workstation.user_setup`
- `cowdogmoo.workstation.package_management`
- `cowdogmoo.workstation.zsh_setup`

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
