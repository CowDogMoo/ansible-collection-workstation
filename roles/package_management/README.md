<!-- DOCSIBLE START -->
# package_management

## Description

Manage package installations and cleanups on Debian-based and Red Hat-based systems

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `package_management_common_install_packages` | list | `[]` | No description |
| `package_management_common_install_packages.0` | str | `autoconf` | No description |
| `package_management_common_install_packages.1` | str | `bash` | No description |
| `package_management_common_install_packages.2` | str | `bison` | No description |
| `package_management_common_install_packages.3` | str | `ca-certificates` | No description |
| `package_management_common_install_packages.4` | str | `colordiff` | No description |
| `package_management_common_install_packages.5` | str | `file` | No description |
| `package_management_common_install_packages.6` | str | `gcc` | No description |
| `package_management_common_install_packages.7` | str | `git` | No description |
| `package_management_common_install_packages.8` | str | `less` | No description |
| `package_management_common_install_packages.9` | str | `make` | No description |
| `package_management_common_install_packages.10` | str | `net-tools` | No description |
| `package_management_common_install_packages.11` | str | `procps` | No description |
| `package_management_common_install_packages.12` | str | `python3` | No description |
| `package_management_common_install_packages.13` | str | `rsync` | No description |
| `package_management_common_install_packages.14` | str | `sudo` | No description |
| `package_management_common_install_packages.15` | str | `terminator` | No description |
| `package_management_common_install_packages.16` | str | `tmux` | No description |
| `package_management_common_install_packages.17` | str | `tree` | No description |
| `package_management_common_install_packages.18` | str | `tzdata` | No description |
| `package_management_common_install_packages.19` | str | `unzip` | No description |
| `package_management_common_install_packages.20` | str | `vim` | No description |
| `package_management_common_install_packages.21` | str | `wget` | No description |
| `package_management_chromium_package` | str | `{{ 'chromium-browser' if ansible_distribution == 'Ubuntu' and ansible_distribution_version is version('20.04', '>=') else 'chromium' }}` | No description |
| `package_management_debian_specific_packages` | list | `[]` | No description |
| `package_management_debian_specific_packages.0` | str | `build-essential` | No description |
| `package_management_debian_specific_packages.1` | str | `{{ package_management_chromium_package }}` | No description |
| `package_management_debian_specific_packages.2` | str | `curl` | No description |
| `package_management_debian_specific_packages.3` | str | `inetutils-ping` | No description |
| `package_management_debian_specific_packages.4` | str | `libdb-dev` | No description |
| `package_management_debian_specific_packages.5` | str | `libffi-dev` | No description |
| `package_management_debian_specific_packages.6` | str | `libgdbm-dev` | No description |
| `package_management_debian_specific_packages.7` | str | `libgdbm6` | No description |
| `package_management_debian_specific_packages.8` | str | `libncurses5-dev` | No description |
| `package_management_debian_specific_packages.9` | str | `libreadline6-dev` | No description |
| `package_management_debian_specific_packages.10` | str | `libssl-dev` | No description |
| `package_management_debian_specific_packages.11` | str | `libyaml-dev` | No description |
| `package_management_debian_specific_packages.12` | str | `locales` | No description |
| `package_management_debian_specific_packages.13` | str | `software-properties-common` | No description |
| `package_management_debian_specific_packages.14` | str | `zlib1g-dev` | No description |
| `package_management_redhat_specific_packages` | list | `[]` | No description |
| `package_management_redhat_specific_packages.0` | str | `bzip2-devel` | No description |
| `package_management_redhat_specific_packages.1` | str | `chromium` | No description |
| `package_management_redhat_specific_packages.2` | str | `epel-release` | No description |
| `package_management_redhat_specific_packages.3` | str | `gcc` | No description |
| `package_management_redhat_specific_packages.4` | str | `gcc-c++` | No description |
| `package_management_redhat_specific_packages.5` | str | `libffi-devel` | No description |
| `package_management_redhat_specific_packages.6` | str | `libtool` | No description |
| `package_management_redhat_specific_packages.7` | str | `openssl-devel` | No description |
| `package_management_redhat_specific_packages.8` | str | `readline-devel` | No description |
| `package_management_redhat_specific_packages.9` | str | `sqlite-devel` | No description |
| `package_management_redhat_specific_packages.10` | str | `zlib-devel` | No description |
| `package_management_install_packages` | str | `<multiline value: folded>` | No description |

## Tasks

### main.yml

- **Set DEBIAN_FRONTEND to noninteractive** (ansible.builtin.lineinfile) - Conditional
- **Install Kali Linux archive keyring** (ansible.builtin.get_url) - Conditional
- **Install packages** (ansible.builtin.package) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - package_management
```

## Author Information

- **Author**: Jayson Grace
- **Company**: CowDogMoo
- **License**: MIT

## Platforms

- Ubuntu: all
- Debian: all
- Kali: all
- EL: all
<!-- DOCSIBLE END -->
