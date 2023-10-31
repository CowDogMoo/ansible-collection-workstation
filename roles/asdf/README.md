# ASDF Role for Ansible

This Ansible role installs and configures
[asdf](https://asdf-vm.com/#/), a CLI tool that can manage multiple language
runtime versions on a per-project basis.

## Requirements

- Ansible version 2.15 or higher

## Supported Platforms

- Ubuntu (all versions)
- macOS (all versions)

## Role Variables

<!--- vars table -->

| Variable                | Default Value (Redhat) | Description                      |
| ----------------------- | ---------------------- | -------------------------------- |
| `asdf_install_packages` | `['git', 'wget']`      | Red Hat packages to be installed |

| Variable                | Default Value (Debian)    | Description                     |
| ----------------------- | ------------------------- | ------------------------------- |
| `asdf_install_packages` | `['curl', 'git', 'wget']` | Debian packages to be installed |

<!--- end vars table -->

## Dependencies

- None

## Example Playbook

```yaml
---
- name: Provision container
  hosts: localhost
  roles:
    - cowdogmoo.workstation.asdf
```

## Molecule Tests

Molecule is used to test the `asdf` role. Tests are located in the
`molecule/default` directory, and can be run with the `molecule test` command.

## License

MIT

## Author Information

- Jayson Grace <jayson.e.grace@gmail.com>
