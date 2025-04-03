# Ansible Collection Release Process

This document outlines the process for creating new releases of the Ansible collection.

## Prerequisites

- [Taskfile](https://taskfile.dev/) installed on your system (`brew install go-task/tap/go-task`)
- [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog)
  installed (`pip install antsibull-changelog`)
- Git repository with proper credentials configured
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
  installed
- [Molecule](https://molecule.readthedocs.io/en/latest/installation.html)
  installed (for testing)
- [act](https://github.com/nektos/act) installed (for GitHub Actions
  local testing)
- [jq](https://stedolan.github.io/jq/download/) installed (for JSON processing)
- Docker installed (required for Molecule and act)

## Pre-Release Tasks

Before creating a release, you should perform these preparation steps:

1. **Run Molecule Tests**

   Run tests to ensure all roles work as expected:

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:run-molecule-tests
   ```

   This command will:

   - Create a logs directory if it doesn't exist
   - Set the ANSIBLE_CONFIG environment variable
   - Run molecule tests for each role directory
   - Log all test output to logs/molecule_tests.log

   Or test a specific role/playbook using GitHub Actions locally:

   ```bash
   # Test a specific role
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:run-molecule-action ROLE=asdf

   # Test a specific playbook
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:run-molecule-action PLAYBOOK=workstation
   ```

   The run-molecule-action task will:

   - Clean up any existing act containers
   - Automatically handle ARM64 architecture on macOS
   - Run the GitHub Actions workflow with the specified role or playbook

1. **Lint Your Ansible Code**

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:lint-ansible
   ```

   This runs ansible-lint with the configuration file at .hooks/linters/ansible-lint.yaml.

1. **Update Collection Dependencies and Versions**

   Update all collection dependencies and version numbers in `requirements.yml`
   and role defaults as needed.

### Changelog Management

The collection uses [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog)
to manage the changelog.

### Creating Changelog Fragments

Add details of changes to the changelog in `changelogs/fragments/` directory.
Create YAML files with appropriate categories:

```yaml
# changelogs/fragments/x.y.z.yaml
---
added:
  - "Description of new feature"
changed:
  - "Description of changes to existing functionality"
removed:
  - "Description of features that were removed"
bugfixes:
  - "Description of bug fixes"
release_summary: "Brief summary of the release"
```

**Important formatting rules:**

- Fragment files should only contain the specific changes for the new version
- Do NOT include the `ancestor` or `releases` sections in fragment files
- Do NOT include a `release_date` field - this is added automatically
- Use YAML list format with hyphens (`-`) for each list item, not indented lists
- Fragment files are automatically deleted after being processed - this is by design

### Managing the Changelog

You can work with the changelog in two ways:

#### Option 1: Run the complete changelog process in one command

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=1.0.0 task ansible:gen-changelog
```

This command will run all the necessary steps (linting and release generation).

#### Option 2: Run individual changelog tasks separately

Lint the changelog first:

```bash
export TASK_X_REMOTE_TASKFILES=1
task ansible:changelog-lint
```

Then generate the release:

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=1.0.0 task ansible:changelog-release
```

**Required Variables:**

- `NEXT_VERSION`: Version number for the release (e.g., 1.0.0)

Example output:

```bash
task: [ansible:gen-changelog] Generating changelog for release 1.0.0
task: [ansible:changelog-lint] antsibull-changelog lint
task: [ansible:changelog-release] antsibull-changelog release --version $NEXT_VERSION
```

## Complete Release Process

Follow these steps to create a new release:

1. **Run Tests and Linting**

   Ensure all tests pass and code is linted:

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:run-molecule-tests
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:lint-ansible
   ```

1. **Update Documentation**

   Ensure all documentation is up-to-date, including README files and role documentation.

1. **Generate Changelog**

   **Option 1: Complete changelog process in one command**

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=x.y.z task ansible:gen-changelog
   ```

   **Option 2: Run individual changelog tasks**

   ```bash
   # First lint the changelog
   export TASK_X_REMOTE_TASKFILES=1
   task ansible:changelog-lint

   # Then generate the release (this will also update galaxy.yml)
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=x.y.z task ansible:changelog-release
   ```

   **Note:** When these commands run, antsibull-changelog will process your
   fragment files, incorporate their content into the main changelog, and then
   automatically remove the fragment files from the filesystem. This is normal
   behavior.

1. **Create a Release Commit**

   ```bash
   git add .
   git commit -m "Release version x.y.z"
   ```

1. **Push Changes**

   ```bash
   git push origin main
   ```

1. **Create GitHub Release and Tag**

   ```bash
   # This creates both a GitHub release and a git tag
   gh release create x.y.z --generate-notes
   ```

   This command uses the GitHub CLI to:

   - Create a new release with the specified version
   - Generate release notes automatically based on commits since the last release
   - Create a corresponding git tag

1. **Build and Publish Collection**

   If using Ansible Galaxy:

   ```bash
   ansible-galaxy collection build
   ansible-galaxy collection publish ./your-namespace-collection-x.y.z.tar.gz
   ```

## Release Versioning

We follow semantic versioning (SemVer) for this collection:

- **Major version** (x.0.0): Incompatible API changes
- **Minor version** (0.x.0): Add functionality in a backward-compatible manner
- **Patch version** (0.0.x): Backward-compatible bug fixes

## Troubleshooting

If you encounter issues with the changelog generation:

1. **Validation Errors**: Check the format of your changelog fragment files
1. **Missing antsibull-changelog**: Install with `pip install antsibull-changelog`
1. **Git Issues**: Ensure your git configuration is correct and you have the
   necessary permissions
1. **Log Files**: Check logs in `logs/molecule_tests.log` for testing issues
