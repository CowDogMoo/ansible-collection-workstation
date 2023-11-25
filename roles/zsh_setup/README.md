# Ansible Role: ZSH Setup

This role installs and configures `zsh` with `oh-my-zsh` for user accounts on
Unix-like systems.

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

| Variable                         | Default Value                                                           | Description                                                                       |
| -------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| zsh_setup_omz_install_script_url | "https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh" | URL for oh-my-zsh install script                                                  |
| zsh_setup_theme                  | "af-magic"                                                              | Default theme for zsh                                                             |
| zsh_setup_default_username       | {{ ansible_distribution \| lower }}                                     | Default username based on the Ansible distribution                                |
| zsh_setup_users                  | Configurable                                                            | List of users for zsh setup. Each user dictionary includes username and usergroup |

### Default Configuration for `zsh_setup_users`

The `zsh_setup_users` variable is a list of dictionaries, each containing:

- `username`: Specified user or default `{{ zsh_setup_default_username }}`
- `usergroup`: User's group, default is `{{ zsh_setup_default_username }}`

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.zsh_setup"
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

1. Check if .oh-my-zsh exists for users.
2. Download oh-my-zsh install script for users.
3. Install oh-my-zsh for users.
4. Check and ensure zsh-installer.sh is executable.
5. Execute zsh-installer.sh for users.
6. Remove zsh-installer.sh after installation.
7. Create per-user $HOME/.zshrc files.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

- `cowdogmoo.workstation.package_management`

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
