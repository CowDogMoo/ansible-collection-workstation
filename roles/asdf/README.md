# Ansible Role: ASDF

This Ansible role manages the installation and configuration of `asdf`, a tool
to manage multiple runtime versions of languages, frameworks, and databases.

---

## Requirements

- Ansible 2.14 or higher.
- Python packages. Install with:

  ```bash
  python3 -m pip install --upgrade \
    ansible-core \
    molecule \
    molecule-docker \
    "molecule-plugins[docker]"
  ```

## Role Variables

| Variable              | Default Value                         | Description                            |
| --------------------- | ------------------------------------- | -------------------------------------- |
| asdf_git_repo         | "https://github.com/asdf-vm/asdf.git" | Git URL for asdf repository            |
| asdf_os_family        | "{{ ansible_os_family \| lower }}"    | OS family for loading specific tasks   |
| asdf_default_username | "{{ ansible_distribution \| lower }}" | Default username based on distribution |
| asdf_users            | Configurable                          | List of users for asdf setup           |

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.asdf"
```

## Testing

For local testing:

- Use [act](https://github.com/nektos/act) for local GitHub Actions testing.

- Run Molecule tests:

  ```bash
  ACTION="molecule"
  if [[ $(uname) == "Darwin" ]]; then
    act -j $ACTION --container-architecture linux/amd64
  fi
  ```

To test changes made to this role locally:

```bash
molecule create
molecule converge
molecule idempotence
molecule destroy
```

## Role Tasks

The role includes tasks for:

- Checking and installing libyaml.
- Setting up asdf environment for each user.
- Cloning and updating asdf repository.
- Deploying and managing tool versions.
- Updating shell profiles with asdf setup.
- Installing and configuring asdf packages.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- macOS
- EL (Enterprise Linux)

## Dependencies

- role: cowdogmoo.workstation.user_setup

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
