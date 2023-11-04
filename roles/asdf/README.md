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
| Variable | Default Value | Description |
| --- | --- | --- |
| `asdf_dest_folder` | `{{ ansible_env.HOME }}/.asdf` | Destination folder for cloning the asdf repository |
| `asdf_install_for_all_users` | `False` | Set to true to install for all users |
| `asdf_git_repo` | `https://github.com/asdf-vm/asdf.git` | Git repository URL of asdf |
| `asdf_languages` | `golang, python, ruby` | Languages to configure with asdf |
| `asdf_os_family` | `{{ ansible_os_family \| lower }}` | OS family variable used for loading OS-specific tasks |
| `asdf_setup_script` | `/tmp/setup_asdf.sh` | Local path to the setup script |
| `asdf_setup_script_url` | `https://raw.githubusercontent.com/l50/dotfiles/main/files/setup_asdf.sh` | URL to download the setup script |
| `asdf_tool_versions` | `{{ ansible_env.HOME }}/.tool-versions` | Path to the `.tool-versions` file |
| `asdf_tool_versions_url` | `https://raw.githubusercontent.com/l50/dotfiles/main/.tool-versions` | URL to download the `.tool-versions` file |
| `asdf_users` | `None` | Users to setup with asdf |
| `- username` | `root` |  |
| `usergroup` | `root` |  |
| Variable | Default Value (Debian) | Description |
| --- | --- | --- |
| `asdf_install_packages` | `curl, git, wget` | Debian packages to be installed |
| Variable | Default Value (Redhat) | Description |
| --- | --- | --- |
| `asdf_install_packages` | `git, wget` | Red Hat packages to be installed |
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
