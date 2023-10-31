# Ansible Role: vnc + oh-my-zsh

[![Pre-Commit](https://github.com/cowdogmoo/ansible_vnc_zsh/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/cowdogmoo/ansible_vnc_zsh/actions/workflows/pre-commit.yml)
[![Molecule Test](https://github.com/cowdogmoo/ansible_vnc_zsh/actions/workflows/molecule.yml/badge.svg)](https://github.com/cowdogmoo/ansible_vnc_zsh/actions/workflows/molecule.yml)
[![Ansible Galaxy](https://img.shields.io/badge/Galaxy-cowdogmoo.vnc_zsh-660198.svg?style=flat)](https://galaxy.ansible.com/ui/standalone/roles/CowDogMoo/vnc_zsh)
[![License](https://img.shields.io/github/license/CowDogMoo/ansible_vnc_zsh?label=License&style=flat&color=blue&logo=github)](https://github.com/CowDogMoo/ansible_vnc_zsh/blob/main/LICENSE)

This role installs [vnc](https://tigervnc.org/) and
[oh-my-zsh](https://ohmyz.sh/) on Debian-based systems.

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

<!--- vars table -->
| Variable | Default Value | Description |
| --- | --- | --- |

| Variable | Default Value (Debian) | Description |
| --- | --- | --- |
| `vnc_zsh_users` | `None` | List of users for whom vnc is to be configured |
| `- username` | `{{ vnc_zsh_default_username }}` |  |
| `usergroup` | `{{ vnc_zsh_default_username }}` |  |
| `sudo` | `True` |  |
| `vnc_num` | `1` |  |
| `vnc_zsh_default_username` | `{{ ansible_distribution \| lower }}` | Default username value, derived from the ansible_distribution variable |
| `vnc_zsh_cleanup_packages` | `xfce4-power-manager` | List of packages to be removed as part of the cleanup process |
| `vnc_zsh_install_packages` | `bash, ca-certificates, colordiff, curl, dbus-x11, file, fonts-powerline, git, inetutils-ping, less, locales, net-tools, rsync, software-properties-common, sudo, terminator, tigervnc-standalone-server, tigervnc-tools, wget, vim, xfce4, xfce4-goodies, zsh, zsh-autosuggestions` | List of packages to be installed for vnc and zsh setup |
<!--- end vars table -->

Available variables are listed below, along with default values (see `defaults/main.yml`):

Path to clone [vncpwd](https://github.com/jeroennijhof/vncpwd).

```yaml
vnc_zsh_vncpwd_clone_path: /tmp/vncpwd
```

URL for the oh-my-zsh install script.

```yaml
vnc_zsh_omz_install_script_url: "https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh"
```

URL to clone [vncpwd](https://github.com/jeroennijhof/vncpwd) from.

```yaml
vnc_zsh_vncpwd_repo_url: https://github.com/jeroennijhof/vncpwd.git
```

Location on disk to install vncpwd.

```yaml
vnc_zsh_vncpwd_path: /usr/local/bin/vncpwd
```

Client options for `vnc`.

```yaml
vnc_zsh_vnc_client_options: "-geometry 1920x1080 --localhost no"
```

Specify whether to setup a systemd service to manage
the vnc installation. Worth considering if you are
using this role outside of a container.

```yaml
vnc_zsh_setup_systemd: false
```

Oh-my-zsh theme to install.

```yaml
vnc_zsh_theme: "af-magic"
```

**Debian-specific vars:**

Users to configure `vnc` for.

```yaml
vnc_zsh_users:
  - username: "ubuntu"
    usergroup: "ubuntu"
    sudo: true
    vnc_num: 1
```

Required packages for the installation.

```yaml:
vnc_zsh_install_packages:
  - bash
  - ca-certificates
  - colordiff
  - curl
...
```

---

## Local Development

Make sure to run the following to develop locally:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.vnc_zsh"
```

---

## Get vnc password

A random 8-character password is generated when the role
is run initially. To retrieve it, run this command on the
provisioned system:

```bash
/usr/local/bin/vncpwd /home/ubuntu/.vnc/passwd
```

---

## Testing

To test actions locally, you can install [act](https://github.com/nektos/act)
and use the following command:

```bash
ACTION="molecule"
if [[ $(uname) == "Darwin" ]]; then
  act -j $ACTION --container-architecture linux/amd64
fi
```

To test changes made to this role locally, run the following commands:

```bash
molecule create
molecule converge
molecule idempotence
# If everything passed, tear down the docker container spawned by molecule:
molecule destroy
```
