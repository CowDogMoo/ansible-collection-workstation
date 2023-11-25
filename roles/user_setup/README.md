# Ansible Role: User Setup

This role sets up user accounts with optional sudo privileges for Unix-like systems.

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

| Variable                    | Default Value                       | Description                                                                                  |
| --------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------- |
| user_setup_install_packages | ["bash", "sudo"]                    | Base packages to install                                                                     |
| user_setup_default_username | {{ ansible_distribution \| lower }} | Default username based on the Ansible distribution                                           |
| user_setup_default_users    | Configurable                        | List of users with attributes: username, usergroup, sudo, shell (defaults provided in below) |

### Default Configuration for `user_setup_default_users`

The `user_setup_default_users` variable is a list of dictionaries, each containing:

- `username`: Default is `{{ user_setup_default_username }}`
- `usergroup`: Group of the user, default is `{{ user_setup_default_username }}`
- `sudo`: Whether the user has sudo access, default is `true`
- `shell`: Default shell for the user, default is `/bin/zsh`

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.user_setup"
```

## Testing

For local testing:

- Install [act](https://github.com/nektos/act) for running GitHub Actions locally.

- Run:

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

1. Gather the list of unique shells to install.
2. Install base packages.
3. Install user-specific shells.
4. Ensure groups exist for users.
5. Create users.
6. Provide sudoers access for relevant users.

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
