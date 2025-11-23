<!-- DOCSIBLE START -->
# package_management

## Description

Manage package installations and cleanups on Debian-based and Red Hat-based systems

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| ---------- | ------ | --------- | ------------- |
| `package_management_common_install_packages` | list | <code>&#91;&#93;</code> | No description |
| `package_management_common_install_packages.0` | str | <code>autoconf</code> | No description |
| `package_management_common_install_packages.1` | str | <code>bash</code> | No description |
| `package_management_common_install_packages.2` | str | <code>bison</code> | No description |
| `package_management_common_install_packages.3` | str | <code>ca-certificates</code> | No description |
| `package_management_common_install_packages.4` | str | <code>colordiff</code> | No description |
| `package_management_common_install_packages.5` | str | <code>file</code> | No description |
| `package_management_common_install_packages.6` | str | <code>gcc</code> | No description |
| `package_management_common_install_packages.7` | str | <code>git</code> | No description |
| `package_management_common_install_packages.8` | str | <code>less</code> | No description |
| `package_management_common_install_packages.9` | str | <code>make</code> | No description |
| `package_management_common_install_packages.10` | str | <code>net-tools</code> | No description |
| `package_management_common_install_packages.11` | str | <code>procps</code> | No description |
| `package_management_common_install_packages.12` | str | <code>python3</code> | No description |
| `package_management_common_install_packages.13` | str | <code>rsync</code> | No description |
| `package_management_common_install_packages.14` | str | <code>sudo</code> | No description |
| `package_management_common_install_packages.15` | str | <code>terminator</code> | No description |
| `package_management_common_install_packages.16` | str | <code>tmux</code> | No description |
| `package_management_common_install_packages.17` | str | <code>tree</code> | No description |
| `package_management_common_install_packages.18` | str | <code>tzdata</code> | No description |
| `package_management_common_install_packages.19` | str | <code>unzip</code> | No description |
| `package_management_common_install_packages.20` | str | <code>vim</code> | No description |
| `package_management_common_install_packages.21` | str | <code>wget</code> | No description |
| `package_management_chromium_package` | str | <code>{{ 'chromium-browser' if ansible_distribution == 'Ubuntu' and ansible_distribution_version is version('20.04', '>=') else 'chromium' }}</code> | No description |
| `package_management_debian_specific_packages` | list | <code>&#91;&#93;</code> | No description |
| `package_management_debian_specific_packages.0` | str | <code>build-essential</code> | No description |
| `package_management_debian_specific_packages.1` | str | <code>{{ package_management_chromium_package }}</code> | No description |
| `package_management_debian_specific_packages.2` | str | <code>curl</code> | No description |
| `package_management_debian_specific_packages.3` | str | <code>inetutils-ping</code> | No description |
| `package_management_debian_specific_packages.4` | str | <code>libdb-dev</code> | No description |
| `package_management_debian_specific_packages.5` | str | <code>libffi-dev</code> | No description |
| `package_management_debian_specific_packages.6` | str | <code>libgdbm-dev</code> | No description |
| `package_management_debian_specific_packages.7` | str | <code>libgdbm6</code> | No description |
| `package_management_debian_specific_packages.8` | str | <code>libncurses5-dev</code> | No description |
| `package_management_debian_specific_packages.9` | str | <code>libreadline6-dev</code> | No description |
| `package_management_debian_specific_packages.10` | str | <code>libssl-dev</code> | No description |
| `package_management_debian_specific_packages.11` | str | <code>libyaml-dev</code> | No description |
| `package_management_debian_specific_packages.12` | str | <code>locales</code> | No description |
| `package_management_debian_specific_packages.13` | str | <code>software-properties-common</code> | No description |
| `package_management_debian_specific_packages.14` | str | <code>zlib1g-dev</code> | No description |
| `package_management_redhat_specific_packages` | list | <code>&#91;&#93;</code> | No description |
| `package_management_redhat_specific_packages.0` | str | <code>bzip2-devel</code> | No description |
| `package_management_redhat_specific_packages.1` | str | <code>chromium</code> | No description |
| `package_management_redhat_specific_packages.2` | str | <code>epel-release</code> | No description |
| `package_management_redhat_specific_packages.3` | str | <code>gcc</code> | No description |
| `package_management_redhat_specific_packages.4` | str | <code>gcc-c++</code> | No description |
| `package_management_redhat_specific_packages.5` | str | <code>libffi-devel</code> | No description |
| `package_management_redhat_specific_packages.6` | str | <code>libtool</code> | No description |
| `package_management_redhat_specific_packages.7` | str | <code>openssl-devel</code> | No description |
| `package_management_redhat_specific_packages.8` | str | <code>readline-devel</code> | No description |
| `package_management_redhat_specific_packages.9` | str | <code>sqlite-devel</code> | No description |
| `package_management_redhat_specific_packages.10` | str | <code>zlib-devel</code> | No description |
| `package_management_install_packages` | str | <code><multiline value: folded></code> | No description |

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
