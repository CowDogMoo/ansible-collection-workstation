# Ansible Role: VNC Setup

This role configures VNC services with systemd integration, ensuring isolated
and secure remote desktop access for each user on Unix-like systems.

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

| Variable                    | Default Value                                                     | Description                                         |
| --------------------------- | ----------------------------------------------------------------- | --------------------------------------------------- |
| vnc_setup_vncpwd_repo_url   | [vncpwd Git repo URL](https://github.com/jeroennijhof/vncpwd.git) | URL for cloning vncpwd repo.                        |
| vnc_setup_client_options    | "-geometry 1920x1080"                                             | Options for VNC client configuration.               |
| vnc_setup_systemd           | true                                                              | Determines if systemd services are set up.          |
| vnc_setup_users             | Configurable                                                      | List of users to set up with VNC.                   |
| vnc_setup_default_username  | "{{ ansible_distribution \| lower }}"                             | Default username derived from ansible_distribution. |
| vnc_setup_vncpwd_clone_path | "/tmp/vncpwd"                                                     | Path to clone vncpwd repo.                          |
| vnc_setup_vncpwd_path       | "/usr/local/bin/vncpwd"                                           | Path to install vncpwd executable.                  |

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.vnc_setup"
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

1. Install and configure vncpwd.
2. Set up user-specific .vnc directories.
3. Generate random VNC passwords.
4. Create user runtime directories.
5. Enable lingering and systemd directories for users.
6. Configure VNC service files and permissions.
7. Add scripts to start VNC and set XDG_RUNTIME_DIR.

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
