============================================================
CowDogMoo Workstation Ansible Collection 1.6.0 Release Notes
============================================================

.. contents:: Topics

v1.6.0
======

Release Summary
---------------

Enhancements in GitHub Actions workflows, updates to the `asdf` role, and general improvements.

Added
-----

- Added `molecule-plugins[docker]` to the dependencies in the Molecule GitHub Actions workflow.
- Added condition to exclude `root` user in `asdf_get_enriched_users.yml`.
- Added content-based `.tool-versions` file deployment in `main.yml`.
- Added initialization of `asdf_enriched_users` in `asdf_get_enriched_users.yml`.
- Added update functionality to the ASDF clone task in `main.yml`.

Changed
-------

- Changed the symlink creation path in the Molecule GitHub Actions workflow to use `$HOME`.
- Modified the `asdf_get_enriched_users.yml` task to ensure user home directory exists.
- Refactored the installation of dependencies in the Molecule GitHub Actions workflow.
- Removed the template for `.tool-versions` file.
- Simplified the deployment of `.tool-versions` file in `main.yml`.
- Updated GitHub Actions setup-python step to a new version.
- Updated Renovate Bot GitHub Action to a new version.
- Updated plugin versions in `asdf` role defaults.
- Updated the ASDF clone task to fetch updates if the repository already exists.

v1.5.0
======

Added
-----

- Added `getent` task to `asdf` and `zsh_setup` roles for fetching local user info
- Added docstring for new plugin; minor QOL updates
- Added macOS compatibility with custom `getent_passwd` plugin
- Debugging for enriched_asdf_enriched_users in asdf main task
- Shell specification for MacOSX in workstation playbook
- Task to ensure asdf directory is cloned for each user in asdf role
- Task to ensure user home directory exists before cloning asdf
- Updated `asdf` and `zsh_setup` roles to dynamically resolve user home directories

Changed
-------

- Adjusted `zsh_setup_get_enriched_users.yml` to align with changes in user creation and home directory setup
- Adjusted file and directory paths in asdf tasks to use `item.home`
- Adjusted loops in `asdf` role's `package_individual_setup.yml` for consistency
- Cleaned up unused variables in `zsh_setup` defaults and molecule verification
- Defined `zsh_setup_users` in zsh_setup main task for clarity
- Fixed issues with handling undefined `plugins` attribute in the `asdf` role
- Fixed naming scheme of enriched asdf users
- Included default variables in zsh_setup molecule verification
- Modified `asdf_get_enriched_users.yml`, `main.yml` in `user_setup`, and `zsh_setup_get_enriched_users.yml` to conditionally use `getent_passwd` module on macOS systems
- Modified `zsh_setup` role to ensure `shell` attribute is defined for users and to use Ansible's user module for creating users and home directories
- Modified main tasks in `asdf` and `zsh_setup` roles to use updated user variables
- Refactored `asdf_get_enriched_users.yml` and `zsh_setup_get_enriched_users.yml`
- Refactored `asdf_get_enriched_users.yml` to use Ansible's user module for creating users and home directories, eliminating the need for `getent`
- Refactored workstation playbook and roles for idempotency and user existence checks
- Removed redundant `set_fact` task in `zsh_setup` main.yml
- Renamed platform names in zsh_setup molecule configuration
- Resolved undefined variable errors related to the `shell` attribute in the `zsh_setup` role
- Simplified variable names and usage in asdf role
- Updated `getent` tasks to exclude macOS systems, ensuring compatibility
- Updated `main.yml` and `package_individual_setup.yml` in the asdf role to handle undefined `plugins` attribute more gracefully
- Updated asdf clone task to use `item.home` and added `become` statements
- Updated file and directory paths in zsh_setup verification tasks
- Updated paths and variable usage in zsh_setup tasks
- Updated shell profile update task in asdf role
- Updated user_setup to use ansible_facts for getent_passwd

Removed
-------

- Removed redundant user creation tasks in `asdf` and `zsh_setup` roles that were causing idempotency issues in playbooks

v1.4.0
======

Release Summary
---------------

Significant enhancements to asdf role, introduction of Molecule tests, and configuration improvements in this release.

Added
-----

- Enhanced asdf role with user-specific setup scripts.
- Logging configuration enhancements in the logging role.
- Molecule testing configurations for `attack-box` playbook.
- Package management improvements for different distributions.
- User setup and zsh setup roles in `attack-box.yml`.

Changed
-------

- Changed hosts from localhost to all in `attack-box.yml`.
- Simplified package management role with unified tasks for Debian and RedHat.
- Updated asdf role to remove OS-specific tasks and focus on user-based configuration.

Removed
-------

- Deprecated vnc_zsh role and associated files in favor of streamlined setup.
- Removed Windows support in asdf role's documentation.

v1.3.0
======

Release Summary
---------------

Extended `asdf` role functionality and improved project configurations.

Added
-----

- Enhanced asdf role with user-specific setup scripts.
- Logging configuration enhancements in the logging role.
- Molecule testing configurations for `attack-box` playbook.
- Package management improvements for different distributions.
- User setup and zsh setup roles in `attack-box.yml`.

Changed
-------

- Changed hosts from localhost to all in `attack-box.yml`.
- Simplified package management role with unified tasks for Debian and RedHat.
- Updated asdf role to remove OS-specific tasks and focus on user-based configuration.

Removed
-------

- Deprecated vnc_zsh role and associated files in favor of streamlined setup.
- Removed Windows support in asdf role's documentation.

v1.2.0
======

Release Summary
---------------

Refactored `asdf` and created new `vnc_zsh` role enhancing functionality.

Added
-----

- Failure conditions in `asdf` role's `check-and-download.yml`.
- Molecule setup for testing `vnc_zsh` role with various scenarios.
- OS-specific setup tasks and variables for Debian in `vnc_zsh` role.
- Unified `asdf_install_packages` variable for package installation.
- Variables, tasks, templates for configuring VNC and ZSH in `vnc_zsh` role.

Changed
-------

- Restructured table, moved variables, modified tasks in `asdf` role.
- Updated package installation tasks in `asdf` role's `setup-debian.yml`, `setup-redhat.yml`.

Removed
-------

- Windows support, redundant block in `asdf` role's `README.md` and `tasks/main.yml`.

v1.1.0
======

Release Summary
---------------

Extended `asdf` role functionality and improved project configurations.

Added
-----

- Added `ansible-galaxy` collection installation from GitHub repository in GitHub Actions workflow.
- Documentation Generation Hook: Implemented a pre-commit hook for automated documentation generation of Go packages.
- New Example Provision Playbook: Added `provision.yml` in the examples directory illustrating the usage of the `asdf` role.
- RedHat Specific Tasks: Created `setup-redhat.yml` for RedHat specific setup tasks within the `asdf` role.
- RedHat Support: Added support for RedHat-based systems in the `asdf` role.
- Shell Profile Update: Automated the update of shell profiles with ASDF settings ensuring idempotency.
- Test Enhancements: Expanded Molecule tests to verify the `asdf` role on RedHat and Debian-based systems.

Changed
-------

- ASDF Setup Logic: Modified the ASDF setup logic in `asdf` role for better clarity and maintainability.
- Error Handling Improvement: Corrected the error handling in `magefile.go` to reflect the correct variable.
- File Renames: Renamed linting configuration files to remove leading dots and comply with standard naming conventions.
- Refactored `pre-commit.yaml` to add new hooks for checking symlinks, private keys, and ensuring shebang scripts are executable.
- Refactored file addition in `pre-commit.yaml` to use a single `git add` command.
- Shell Profile Update: Enhanced the shell profile update tasks in `asdf` role to ensure idempotency and clarity.
- Updated `README.md` in both the repository root and `roles/asdf` directory to reflect new changes and provide clearer instructions.
- Updated `README.md` to reflect the new installation command using `git+https` URL.
- Updated `ansible-lint` and `yamllint` paths in `.pre-commit-config.yaml` to reflect the new file names.
- Updated `molecule.yaml` in GitHub Actions workflow to include `ansible-galaxy` collection installation step.
- Updated minimum Ansible version in `roles/asdf/meta/main.yml` to 2.14

Removed
-------

- Removed the separate ShellCheck repository in `.pre-commit-config.yaml` and consolidated ShellCheck hook under `jumanjihouse/pre-commit-hooks`.

v1.0.0
======

Release Summary
---------------

Added a new `asdf` role

Added
-----

- Added automated documentation generation for magefile utilities
- Automated Release Playbook - Introduced `galaxy-deploy.yml`, an automated release playbook for publishing the collection to Ansible Galaxy.
- Molecule Workflow - Added a new GitHub Actions workflow `molecule.yaml` for running Molecule tests on pull requests and pushes.
- Renovate Bot Configuration - Updated Renovate Bot configurations to reflect the new repository structure and naming.
- `molecule` configuration - Added new `molecule` configuration for the `asdf` role to support local testing and verification.
- asdf role - Added a new `asdf` role with enhanced functionality including OS-specific setup. Updated metadata and created new documentation under `roles/asdf/README.md` detailing role usage and variables.

Changed
-------

- GitHub Actions Workflows - Refactored the `release.yaml` workflow to align with Ansible collection standards, including updating working directory paths, setting up Python, installing dependencies, and automating the release to Ansible Galaxy.
- Pre-commit hooks - Added new pre-commit hooks for shell script validation and formatting.
- Refactored Ansible linting configuration - Moved the `.ansible-lint` configuration to `.ansible-lint.yaml` and adjusted linting rules. Also, added `mdstyle.rb` and `.mdlrc` for markdown linting configurations.
- Repository Metadata - Updated repository links in `README.md` and `galaxy.yml` to reflect the new repository naming and structure.
- Upgrade dependencies - Upgraded versions of pre-commit hooks and dependencies in `.pre-commit-config.yaml`, updated mage's `go.sum` to reflect the new dependency tree, and removed unused dependencies from mage's `go.sum`.

Removed
-------

- Removed old files in preparation for later refactoring.
- Windows Support for asdf role - Removed Windows support from `roles/asdf/README.md` as it is not supported in the tasks.
