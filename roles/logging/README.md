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
| Variable | Default Value | Description |
| --- | --- | --- |
| `logging_directories` | `None` |  |
| `- path` | `/var/log/ansible` |  |
| `owner` | `root` |  |
| `group` | `root` |  |
| `mode` | `0755` |  |
| `logging_log_rotation_defaults` | `None` |  |
| `path` | `/var/log/ansible/*.log` |  |
| `options` | `None` |  |
| `rotate` | `4` |  |
| `frequency` | `weekly` |  |
| `compress` | `True` |  |
| `missingok` | `True` |  |
| `notifempty` | `True` |  |
| `create` | `True` |  |
| `dateext` | `True` |  |

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
