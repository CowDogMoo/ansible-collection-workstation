# Ansible Role: Configure oh-my-zsh with zsh

This role installs and configures [oh-my-zsh](https://ohmyz.sh/) for multiple
users.

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

The role uses the following variables:

- `zsh_setup_omz_install_script_url_url`: URL to the oh-my-zsh install script.
- `zsh_setup_theme`: The theme to be used with oh-my-zsh.
- `zsh_setup_default_username`: Default username (set to the distribution name).
- `zsh_setup_users`: List of users for whom oh-my-zsh will be configured.

## Local Development

To develop locally, run:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.zsh"
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
molecule destroy # To tear down the docker container
```

## Role Tasks

The role includes the following main tasks:

1. Check if `.oh-my-zsh` exists for each user.
2. Download the oh-my-zsh install script.
3. Install oh-my-zsh.
4. Check for the existence of the zsh-installer script.
5. Ensure the zsh-installer script is executable.
6. Execute the zsh-installer script.
7. Remove the zsh-installer script.
8. Create per-user `.zshrc` files.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali Linux
- Rocky Linux

## Dependencies

This role depends on the following roles:

- `cowdogmoo.workstation.package_management`

Ensure these dependencies are installed or available before using this role.

## Author Information

This role was created by [Jayson Grace](https://techvomit.net) and is
maintained as part of the CowDogMoo project.
