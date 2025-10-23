# Ansible Role: fabric

Installs and configures [Daniel Miessler's Fabric](https://github.com/danielmiessler/fabric), an open-source AI framework for augmenting humans using AI prompts.

## Description

This role installs Fabric and creates the necessary configuration directories. It supports multiple installation methods to accommodate different environments and preferences.

## Requirements

Depending on your chosen installation method:

- **go_install** (default): Go must be installed and in PATH
- **script**: curl and bash
- **homebrew**: Homebrew (macOS only)
- **npm**: Node.js and npm

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# User configuration
fabric_username: "{{ ansible_user_id | default(ansible_user) }}"
fabric_usergroup: "{{ (ansible_facts['os_family'] == 'Darwin') | ternary('staff', fabric_username) }}"
fabric_user_home: "{{ ... }}"

# Whether to install Fabric (set to false if you only want to manage config)
fabric_install: true

# Installation method: 'go_install', 'script', 'homebrew', or 'npm'
fabric_install_method: "go_install"

# Package details (for go_install method)
fabric_go_package: "github.com/danielmiessler/fabric@latest"

# Configuration directory for fabric
fabric_config_dir: "{{ fabric_user_home }}/.config/fabric"

# Whether to initialize fabric directories
fabric_init_directories: true

# Whether to run fabric --setup after installation
# Note: This is disabled by default as it requires interactive input
fabric_run_setup: false
```

## Dependencies

None. This role is self-contained and works with whatever Go/npm/brew installation you have.

## Example Playbook

### Using go install (default)

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.fabric
```

### Using the official install script

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.fabric
      vars:
        fabric_install_method: "script"
```

### Using Homebrew (macOS)

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.fabric
      vars:
        fabric_install_method: "homebrew"
```

### Using npm

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.fabric
      vars:
        fabric_install_method: "npm"
```

### Config only (skip installation)

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.fabric
      vars:
        fabric_install: false
```

## Post-Installation

After running this role, you'll need to:

1. Verify Fabric is in your PATH:

   ```bash
   fabric --version
   ```

2. Run the setup command to configure API keys:

   ```bash
   fabric --setup
   ```

3. Update patterns:

   ```bash
   fabric --update
   ```

## Integration with asdf

If you're using asdf to manage Go, you can have asdf automatically install Fabric:

```yaml
- hosts: localhost
  roles:
    - role: cowdogmoo.workstation.asdf
      vars:
        asdf_plugins:
          - name: golang
            version: "1.25.3"
            scope: "global"
            default_packages:
              - github.com/danielmiessler/fabric@latest

    # Only manage fabric config, skip installation
    - role: cowdogmoo.workstation.fabric
      vars:
        fabric_install: false
```

## License

MIT

## Author Information

This role was created by CowDogMoo.
