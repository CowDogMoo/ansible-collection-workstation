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

---

## Role Variables

| Variable                         | Default Value                                                           | Description              |
| -------------------------------- | ----------------------------------------------------------------------- | ------------------------ |
| zsh_setup_omz_install_script_url | "https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh" | oh-my-zsh install script |
| zsh_setup_theme                  | "af-magic"                                                              | Default theme for zsh    |
| zsh_setup_default_username       | {{ ansible_distribution \| lower }}                                     | Default username         |
| zsh_setup_users                  | Configurable                                                            | Users for zsh setup      |

### Default Configuration for `zsh_setup_users`

- `username`: Specified user or default `{{ zsh_setup_default_username }}`
- `usergroup`: User's group, default is `{{ zsh_setup_default_username }}`

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

- Check if .oh-my-zsh exists for users.
- Download oh-my-zsh install script.
- Install oh-my-zsh for users.
- Ensure zsh-installer.sh is executable.
- Execute zsh-installer.sh for users.
- Remove zsh-installer.sh after installation.
- Create per-user $HOME/.zshrc files.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- macOS
- Kali
- EL (Enterprise Linux)

## Dependencies

- `cowdogmoo.workstation.package_management`

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
