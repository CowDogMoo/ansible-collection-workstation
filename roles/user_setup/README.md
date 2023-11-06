# Ansible Role: User Setup

This role sets up user accounts with optional sudo privileges and installs
[zsh](https://www.zsh.org/) for Unix-like systems, supporting Debian and
RedHat-based distributions.

## Requirements

- Python packages

  Install with:

  ```bash
  python3 -m pip install --upgrade \
    ansible-core \
    molecule \
    molecule-docker \
    "molecule-plugins[docker]"
  ```

---

## Role Variables

Here's a table of role variables and their default values:

<!--- vars table -->
| Variable | Default Value | Description |
| --- | --- | --- |
| `user_setup_default_username` | `{{ ansible_distribution \| lower }}` |  |
| `user_setup_default_users` | `None` |  |
| `- username` | `{{ user_setup_default_username }}` |  |
| `usergroup` | `{{ user_setup_default_username }}` |  |
| `sudo` | `True` |  |
| `shell` | `/bin/zsh` |  |
| Variable | Default Value (Debian) | Description |
| --- | --- | --- |
| `user_setup_install_packages` | `bash, sudo` | List of packages to be installed for each user |
| Variable | Default Value (Redhat) | Description |
| --- | --- | --- |
| `user_setup_install_packages` | `bash, sudo` | List of packages to be installed for each user |
<!--- end vars table -->

Note: See `vars/debian.yml` and `vars/redhat.yml` for
distribution-specific package lists.

---

## Testing

To test changes made to this role locally, run the following commands:

```bash
molecule create
molecule converge
molecule idempotence
# If everything passes, tear down the docker container(s) spawned by molecule:
molecule destroy
```

Refer to `./molecule/default/` directory for molecule scenarios and testing configurations.
