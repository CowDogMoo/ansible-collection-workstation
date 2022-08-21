# Ansible Role: homebrew

[![Pre-Commit](https://github.com/metaredteam/ansible-ROLE_NAME/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/metaredteam/ansible-ROLE_NAME/actions/workflows/pre-commit.yaml)
[![Molecule Test](https://github.com/metaredteam/ansible-ROLE_NAME/actions/workflows/molecule.yaml/badge.svg)](https://github.com/metaredteam/ansible-ROLE_NAME/actions/workflows/molecule.yaml)

This role installs [ROLE_NAME](https://github.com/metaredteam/ROLE_NAME) on Linux hosts.

## Requirements

- `community.general.make`

  Install with:

  ```bash
  ansible-galaxy install collections -r requirements.yml
  ```

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

URL of the repository that houses ROLE_NAME.

```yaml
repo_url: https://github.com/metaredteam/ROLE_NAME.git
```

The path where the `ROLE_NAME` repo will be cloned.

```yaml
clone_path: /tmp/ROLE_NAME
```

Installation location for `ROLE_NAME`.

```yaml
tool_path: /usr/local/bin/ROLE_NAME
```

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  roles:
    - role: metaredteam.ROLE_NAME
```

## Local Development

Make sure to run the following to develop locally:

```bash
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/metaredteam.ROLE_NAME"
```

## Testing

To test changes made to this role, run the following commands:

```bash
molecule create
molecule converge
# If everything passed, tear down the docker container spawned by molecule:
molecule destroy
```

# Role Name

A brief description of the role goes here.

## Requirements

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

## Role Variables

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

## Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
