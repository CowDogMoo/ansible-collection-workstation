# Ansible Role: ASDF

This role installs and configures the `asdf` version manager on Unix-like systems.

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

| Variable              | Default Value                         | Description                                |
| --------------------- | ------------------------------------- | ------------------------------------------ |
| asdf_git_repo         | "https://github.com/asdf-vm/asdf.git" | Git repository URL of asdf                 |
| asdf_os_family        | "{{ ansible_os_family \| lower }}"    | OS family variable for OS-specific tasks   |
| asdf_packages         | [golang, python, ruby]                | Languages to configure with asdf           |
| asdf_default_username | "{{ ansible_distribution \| lower }}" | Default username                           |
| asdf_users            | Configurable                          | Users to setup with asdf and their scripts |

---

## Local Development

To develop locally, link this role to your Ansible roles directory:

```bash
ansible-galaxy install -r requirements.yml
ln -s "${PWD}" "${HOME}/.ansible/roles/cowdogmoo.asdf"
```

## Testing

For local testing:

- Use [act](https://github.com/nektos/act) for local GitHub Actions testing.

- Run Molecule tests:

  ```bash
  molecule create
  molecule converge
  molecule idempotence
  molecule destroy
  ```

## Role Tasks

The role includes the following main tasks:

1. Clone `asdf` for each user.
2. Check and download necessary files.
3. Execute setup scripts for each user.
4. Update shell profiles for users.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- macOS
- EL (Enterprise Linux)

## Dependencies

- role: cowdogmoo.workstation.user_setup

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
