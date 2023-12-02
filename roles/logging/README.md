# Ansible Role: Logging

This role creates logging directories and configures
log rotation for a provided path.

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

| Variable                    | Default Value | Description                    |
| --------------------------- | ------------- | ------------------------------ |
| logging_directories         | [See Below]   | Directories for logging        |
| logging_log_rotation_config | [See Below]   | Configuration for log rotation |

### Default Configuration for `logging_directories`

The `logging_directories` variable is a list of dictionaries, each containing:

- `path`: Path of the logging directory, default is `"/var/log/ansible"`
- `owner`: Owner of the directory, default is `"root"`
- `group`: Group of the directory, default is `"root"`
- `mode`: File mode, default is `"0755"`

### Default Configuration for `logging_log_rotation_config`

Default settings for log rotation:

- `path`: Log file path, default is `"/var/log/ansible/*.log"`
- `rotate`: Number of rotations, default is `4`
- `frequency`: Rotation frequency, default is `"weekly"`
- `compress`: Compress old versions, default is `true`
- `missingok`: Ignore missing log files, default is `true`
- `notifempty`: Don't rotate if empty, default is `true`
- `create`: Create new log file, default is `true`
- `dateext`: Use date extension, default is `true`
- `owner`: Owner of the log files, default is `"root"`
- `group`: Group of the log files, default is `"root"`

---

## Local Development

To develop locally, run the following from the repository root:

```bash
ansible-galaxy install -r requirements.yml
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/cowdogmoo.logging"
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

The role includes the following main tasks:

1. Ensure logging directories exist.
2. Set up log rotation.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali
- EL (Enterprise Linux)

## Dependencies

No dependencies.

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
