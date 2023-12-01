# Ansible Role: asdf

This role installs and configures asdf, a version manager for multiple
programming languages.

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
| asdf_git_repo         | "https://github.com/asdf-vm/asdf.git" | Git repository URL for asdf                |
| asdf_os_family        | "{{ ansible_os_family \| lower }}"    | OS family for loading OS-specific tasks    |
| asdf_default_username | "{{ ansible_distribution \| lower }}" | Default username for setup                 |
| asdf_users            | Configurable                          | Users to setup with asdf and their plugins |

### Configuration for `asdf_users`

`asdf_users` is a list of dictionaries, each with:

- `username`: User's name
- `usergroup`: User's group
- `shell`: User's shell (default is "/usr/bin/zsh")
- `shell_profile_lines`: Shell profile settings
- `plugins`: List of asdf plugins to install (name, version, scope)

---

## Local Development

To develop locally, run the following from the repository root:

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

Key tasks in this role:

1. Set default username for Kali systems.
2. Clone asdf for each user.
3. Deploy `.tool-versions` file and set correct permissions.
4. Set permissions for each user's ASDF directory.
5. Update shell profiles for each user.
6. Gather installed ASDF plugins and versions for each user.
7. Copy `setup_asdf_env.sh` to a common location for all users.
8. Install and configure asdf packages for each user.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

- role: cowdogmoo.workstation.user_setup

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
