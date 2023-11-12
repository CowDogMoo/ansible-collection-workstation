# Ansible Role: Logging Setup

This role configures logging for applications on Unix-like systems, ensuring
that logs are properly rotated and maintained. It supports Debian and
RedHat-based distributions.

---

## Requirements

- Ansible version 2.15 or higher

---

## Supported Platforms

- Ubuntu (all versions)
- Kali Linux (all versions)
- EL (all versions)

---

## Role Variables

Here's a table of role variables and their default values:

<!--- vars table -->

| Variable                      | Default Value                                | Description                                                                   |
| ----------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------- |
| `vnc_setup_client_options`    | `-geometry 1920x1080 --localhost no`         | VNC client options                                                            |
| `vnc_setup_systemd`           | `False`                                      | Define whether to setup systemd                                               |
| `vnc_setup_users`             | `None`                                       | Define default users for VNC setup                                            |
| `- username`                  | `root`                                       |                                                                               |
| `usergroup`                   | `root`                                       |                                                                               |
| `vnc_num`                     | `1`                                          |                                                                               |
| `vnc_setup_vncpwd_clone_path` | `/tmp/vncpwd`                                | Path to clone [vncpwd](https://github.com/jeroennijhof/vncpwd).               |
| `vnc_setup_vncpwd_path`       | `/usr/local/bin/vncpwd`                      | Location in $PATH to install [vncpwd](https://github.com/jeroennijhof/vncpwd) |
| `vnc_setup_vncpwd_repo_url`   | `https://github.com/jeroennijhof/vncpwd.git` | Path to clone [vncpwd](https://github.com/jeroennijhof/vncpwd)                |

<!--- end vars table -->

Default values for these variables can be found in `defaults/main.yml`.

---

## Example Playbook

Here's an example of how to use this role:

```yaml
- hosts: all
  roles:
    - role: logging_setup
      logging_directories:
        - "/var/log/myapp"
      logrotate_interval: "daily"
      logrotate_keep: 7
```

---

## Testing with Molecule

This role uses Molecule for testing:

```bash
molecule test
```

This will execute a full test suite, which includes linting with yamllint and
ansible-lint, as well as running the actual Ansible playbook to apply the role.

Refer to the `./molecule/default/` directory for test scenarios and
configuration settings.

---

For more information on the role's capabilities and additional configurations,
inspect the `meta/main.yml`, `tasks/`, and `vars/` directories within the role
structure.
