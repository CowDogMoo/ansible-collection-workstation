# Package Management Role

This Ansible role is designed to manage package installations and cleanups on
Debian-based and Red Hat-based systems. It leverages Ansible best practices to
ensure that the necessary packages are installed and unnecessary ones are
removed, maintaining system hygiene.

## Requirements

- Ansible version 2.14 or higher

## Supported Platforms

- Ubuntu (all versions)
- Debian (all versions)
- Kali (all versions)
- EL (all versions, including Red Hat Enterprise Linux and derivatives)

## Role Variables

The role uses variables from `vars/main.yml` to manage packages. Here's a list
of the primary variables:

<!--- vars table -->

| Variable                                      | Description                                  |
| --------------------------------------------- | -------------------------------------------- |
| `package_management_common_install_packages`  | Packages to install on all supported systems |
| `package_management_redhat_excluded_packages` | Packages to exclude on Red Hat systems       |
| `package_management_common_cleanup_packages`  | Packages to clean up on all systems          |

<!--- end vars table -->

For more detailed information, refer to the `vars/main.yml` file within the role
directory.

## Tasks

Tasks are defined in `tasks/main.yml`. They include:

- Including common variables for package names.
- Merging common and OS-specific packages.
- Installing and cleaning up packages on Debian and Red Hat systems.

Each task is idempotent, ensuring that the desired state is achieved without
repeating actions on subsequent playbook runs.

## Molecule Tests

The `molecule/default` directory contains configuration for testing with
Molecule, including:

- A verification playbook (`verify.yml`) to assert that the correct packages
  are present or absent.
- A Docker-based test environment defined in `molecule.yml` and `converge.yml`
  for Debian and Red Hat platforms.

Tests can be run using the `molecule test` command to ensure that the role
behaves as expected.

## Meta Information

- Role Name: package_management
- Namespace: cowdogmoo
- Author: Jayson Grace
- License: MIT

For more details, see `meta/main.yml`.

## Usage Example

To use this role, include it in your playbook as follows:

```yaml
---
- name: Manage packages
  hosts: all
  roles:
    - cowdogmoo.package_management
```

## License

This role is distributed under the MIT license.

## Author Information

- Jayson Grace (jayson.e.grace@gmail.com)
