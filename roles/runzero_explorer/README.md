# Ansible Role: RunZero Explorer

This role installs and executes the
[runZero Explorer](https://console.runzero.com/deploy/download/explorers)
on Debian, Red Hat, Kali, macOS, and Windows-based systems.

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

- You must have a runZero account to download runZero Explorer.
- Through the runZero console, you must create a download key and set it as
  the `RUNZERO_DOWNLOAD_TOKEN` environment variable before running this role.

---

## Role Variables

- `runzero_explorer_path`: The path where the runZero Explorer binary will be
  installed.
- `runzero_explorer_url`: The base URL for downloading runZero Explorer.
- `runzero_explorer_version_id`: The version ID of the runZero Explorer to
  download.
- `runzero_explorer_log_debug`: Enable or disable debug logging for the runZero
  Agent.
- `runzero_explorer_systemd_enabled`: Enable or disable the creation of a
  systemd service for runZero Explorer.

Package management variables:

- `runzero_explorer_common_install_packages`: Common packages required for
  runZero Explorer.
- `runzero_explorer_kali_packages`: Kali-specific packages required for runZero
  Explorer.
- `runzero_explorer_debian_packages`: Debian-specific packages required for
  runZero Explorer.
- `runzero_explorer_el_packages`: Red Hat Enterprise Linux (EL)-specific
  packages required for runZero Explorer.

---

## Testing

To test the role, use Molecule:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

## Role Tasks

Key tasks in this role:

- Set architecture mapping for runZero Explorer.
- Determine the binary architecture for runZero Explorer.
- Set the unique token for downloading runZero Explorer.
- Create the directory for the runZero Explorer binary.
- Download the runZero Explorer binary.
- Find runZero Agent files (if applicable).
- Get the hash of the existing runZero Explorer file (if applicable).
- Rename the most recent runZero Agent file to the default destination (if applicable).
- Execute runZero Explorer.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Debian
- Kali
- Red Hat Enterprise Linux (EL)
- Windows

## Author Information

This role was created by Jayson Grace and is maintained as part of the
CowDogMoo project.
