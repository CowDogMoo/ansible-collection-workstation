===================================
cowdogmoo.workstation Release Notes
===================================

.. contents:: Topics


v1.0.0
======

Release Summary
---------------

Added a new `asdf` role

Added
-----

- `molecule` configuration - Added new `molecule` configuration for the `asdf` role to support local testing and verification.
- asdf role - Added a new `asdf` role with enhanced functionality including OS-specific setup. Updated metadata and created new documentation under `roles/asdf/README.md` detailing role usage and variables.

Changed
-------

- Pre-commit hooks - Added new pre-commit hooks for shell script validation and formatting.
- Refactored Ansible linting configuration - Moved the `.ansible-lint` configuration to `.ansible-lint.yaml` and adjusted linting rules. Also, added `mdstyle.rb` and `.mdlrc` for markdown linting configurations.
- Upgrade dependencies - Upgraded versions of pre-commit hooks and dependencies in `.pre-commit-config.yaml`, updated mage's `go.sum` to reflect the new dependency tree, and removed unused dependencies from mage's `go.sum`.

Removed
-------

- Removed old files in preparation for later refactoring.
