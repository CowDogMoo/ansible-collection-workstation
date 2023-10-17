# Workstation Ansible Collection

[![License](https://img.shields.io/github/license/CowDogMoo/ansible-collection-workstation?label=License&style=flat&color=blue&logo=github)](https://github.com/CowDogMoo/ansible-collection-workstation/blob/main/LICENSE)
[![Pre-Commit](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/pre-commit.yaml)
[![Molecule Test](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/molecule.yaml/badge.svg)](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/molecule.yaml)
[![Renovate](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/renovate.yaml/badge.svg)](https://github.com/CowDogMoo/ansible-collection-workstation/actions/workflows/renovate.yaml)

This Ansible collection provides a suite of utilities and
applications that I use across my various workstations.

## Requirements

- Ansible 2.15 or higher

## Installation

Install the Workstation collection from Ansible Galaxy:

```bash
ansible-galaxy collection install cowdogmoo.workstation
```

## Roles

### ASDF

Installs and configures ASDF, a version manager for multiple language runtimes.
Check out the [ASDF role README](roles/asdf/README.md) for more details.

## Usage

Include the roles from this collection in your playbook. Here's an example:

```yaml
---
- hosts: all
  collections:
    - cowdogmoo.workstation
  roles:
    - asdf
```

## License

This collection is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details.

## Support

- Repository: [cowdogmoo/ansible-collection-workstation](http://github.com/CowDogMoo/ansible-collection-workstation)
- Issue Tracker: [GitHub Issues](https://github.com/CowDogMoo/ansible-collection-workstation/issues)

## Authors

- Jayson Grace ([techvomit.net](https://techvomit.net))
