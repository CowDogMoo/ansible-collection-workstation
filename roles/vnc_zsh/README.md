# Ansible Role: vnc + oh-my-zsh

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
| `vnc_zsh_vncpwd_clone_path` | `/tmp/vncpwd` | Path to clone [vncpwd](https://github.com/jeroennijhof/vncpwd). |
| `vnc_zsh_omz_install_script_url` | `https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh` | Path to clone [oh-my-zsh](https://github.com/ohmyzsh/ohmyzsh). |
| `vnc_zsh_vncpwd_repo_url` | `https://github.com/jeroennijhof/vncpwd.git` | Path to clone [vncpwd](https://github.com/jeroennijhof/vncpwd) |
| `vnc_zsh_vncpwd_path` | `/usr/local/bin/vncpwd` | Location in $PATH to install [vncpwd](https://github.com/jeroennijhof/vncpwd) |
| `vnc_zsh_vnc_client_options` | `-geometry 1920x1080 --localhost no` | VNC client options |
| `vnc_zsh_setup_systemd` | `False` | Setup systemd service for VNC |
| `vnc_zsh_theme` | `af-magic` | ZSH theme |
| Variable | Default Value (Debian) | Description |
| --- | --- | --- |
| `vnc_zsh_users` | `None` | List of users for whom vnc is to be configured |
| `- username` | `root` |  |
| `usergroup` | `root` |  |
| `sudo` | `True` |  |
| `vnc_num` | `2` |  |
| `vnc_zsh_default_username` | `{{ ansible_distribution \| lower }}` | Default username value, derived from the ansible_distribution variable |
| `vnc_zsh_cleanup_packages` | `xfce4-power-manager` | List of packages to be removed as part of the cleanup process |
| `vnc_zsh_install_packages` | `bash, ca-certificates, colordiff, curl, dbus-x11, file, fonts-powerline, git, inetutils-ping, less, locales, net-tools, procps, rsync, software-properties-common, sudo, terminator, tigervnc-standalone-server, tigervnc-tools, wget, vim, xfce4, xfce4-goodies, zsh, zsh-autosuggestions` | List of packages to be installed for vnc and zsh setup |
<!--- end vars table -->

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