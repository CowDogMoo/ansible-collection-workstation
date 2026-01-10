<!-- DOCSIBLE START -->
# build_cleanup

## Description

General-purpose, parameterized cleanup role for build artifact minimization

## Requirements

- Ansible >= 2.15

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `build_cleanup_enabled` | bool | <code>False</code> | No description |
| `build_cleanup_fast_mode` | bool | <code>False</code> | No description |
| `build_cleanup_preserve_includes` | bool | <code>False</code> | No description |
| `build_cleanup_generate_post_script` | bool | <code>True</code> | No description |
| `build_cleanup_install_path` | str | <code></code> | No description |
| `build_cleanup_user_home` | str | <code></code> | No description |
| `build_cleanup_username` | str | <code></code> | No description |
| `build_cleanup_keep_binaries` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_protected_packages` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_source_directories` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_paths` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_packages_debian` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_packages_redhat` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_binary_version_flag` | str | <code>version</code> | No description |
| `build_cleanup_additional_paths` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_container_remove_packages` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_check_unpacked_compilers` | bool | <code>False</code> | No description |
| `build_cleanup_compiler_paths` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_handle_postgresql` | bool | <code>False</code> | No description |
| `build_cleanup_handle_perl` | bool | <code>False</code> | No description |
| `build_cleanup_handle_systemd` | bool | <code>False</code> | No description |
| `build_cleanup_python_keep_packages` | list | <code>&#91;&#93;</code> | No description |
| `build_cleanup_post_script_path` | str | <code>/tmp/post_ansible_cleanup.sh</code> | No description |
| `build_cleanup_clear_histories` | bool | <code>True</code> | No description |
| `build_cleanup_final_apt_cleanup` | bool | <code>True</code> | No description |
| `build_cleanup_final_temp_cleanup` | bool | <code>True</code> | No description |
| `build_cleanup_final_sync` | bool | <code>True</code> | No description |
| `build_cleanup_virtualization_type` | str | <code>{{ ansible_facts&#91;'virtualization_type'&#93; &#124; default('') }}</code> | No description |
| `build_cleanup_is_container` | str | <code>{{ build_cleanup_virtualization_type in &#91;'docker', 'container', 'podman'&#93; }}</code> | No description |
| `build_cleanup_os_family` | str | <code>{{ ansible_facts&#91;'os_family'&#93; &#124; default('Debian') }}</code> | No description |

## Tasks

### apt_cleanup.yml


- **Run apt-get clean** (ansible.builtin.apt)
- **Run apt-get autoclean** (ansible.builtin.apt)
- **Run apt-get autoremove** (ansible.builtin.apt) - Conditional
- **Remove APT cache files** (ansible.builtin.file)
- **Remove APT lists** (ansible.builtin.file)
- **Recreate APT lists directory (required for future apt operations)** (ansible.builtin.file)
- **Recreate APT archives directory** (ansible.builtin.file)
- **Remove dpkg status files** (ansible.builtin.file)
- **Remove downloaded package files** (ansible.builtin.shell)
- **Display APT cleanup summary** (ansible.builtin.debug)

### cleanup_python.yml


- **Find and remove Python cache directories** (ansible.builtin.find)
- **Remove Python cache directories** (ansible.builtin.file) - Conditional
- **Find and remove .pyc and .pyo files** (ansible.builtin.find)
- **Remove .pyc and .pyo files** (ansible.builtin.file) - Conditional
- **Remove pip cache** (ansible.builtin.file)
- **Remove Python test and development packages** (ansible.builtin.file)
- **Clean pip cache via command** (ansible.builtin.command)
- **Display Python cleanup summary** (ansible.builtin.debug)

### container_optimizations.yml


- **Remove container-specific unnecessary packages (Debian)** (ansible.builtin.apt) - Conditional
- **Remove common unnecessary packages in containers (Debian)** (ansible.builtin.apt) - Conditional
- **Remove systemd journal logs** (ansible.builtin.file)
- **Truncate log files instead of deleting** (ansible.builtin.shell)
- **Remove apt cache and lists** (ansible.builtin.file) - Conditional
- **Remove unnecessary kernel files (containers don't need these)** (ansible.builtin.file)
- **Remove firmware (not needed in containers)** (ansible.builtin.file)
- **Display container optimization summary** (ansible.builtin.debug)

### deep_cleanup.yml


- **Remove documentation directories** (ansible.builtin.file)
- **Remove locale files (keep only en_US.UTF-8)** (ansible.builtin.shell)
- **Remove i18n files (internationalization)** (ansible.builtin.shell)
- **Remove unnecessary include files** (ansible.builtin.file) - Conditional
- **Remove static libraries** (ansible.builtin.shell)
- **Remove pkg-config files** (ansible.builtin.shell)
- **Remove systemd (if configured)** (block) - Conditional
- **Remove systemd directories** (ansible.builtin.file)
- **Remove PostgreSQL (if configured)** (block) - Conditional
- **Stop PostgreSQL service** (ansible.builtin.systemd)
- **Remove PostgreSQL data and config** (ansible.builtin.file)
- **Remove Perl (if configured)** (block) - Conditional
- **Remove Perl packages** (ansible.builtin.apt) - Conditional
- **Remove Perl directories** (ansible.builtin.file)
- **Check for unpacked compilers (if configured)** (block) - Conditional
- **Check for unpacked compiler archives** (ansible.builtin.find)
- **Remove unpacked compiler directories** (ansible.builtin.file) - Conditional
- **Remove misc caches and temporary files** (ansible.builtin.file)
- **Recreate var/tmp directory** (ansible.builtin.file)
- **Display deep cleanup summary** (ansible.builtin.debug)

### generate_post_ansible_script.yml


- **Generate post-Ansible cleanup script** (ansible.builtin.template)
- **Verify script was created** (ansible.builtin.stat)
- **Display script generation success** (ansible.builtin.debug) - Conditional
- **Warning if script generation failed** (ansible.builtin.debug) - Conditional

### main.yml


- **Display cleanup configuration** (ansible.builtin.debug) - Conditional
- **Validate required parameters** (ansible.builtin.assert) - Conditional
- **Execute cleanup phases** (block) - Conditional
- **Phase 1: Protect packages from autoremoval** (ansible.builtin.include_tasks) - Conditional
- **Phase 2: Remove build artifacts** (ansible.builtin.include_tasks)
- **Phase 3: Optimize binaries** (ansible.builtin.include_tasks) - Conditional
- **Phase 4: Remove development packages** (ansible.builtin.include_tasks) - Conditional
- **Phase 5: Cleanup Python artifacts** (ansible.builtin.include_tasks)
- **Phase 6: Container-specific optimizations** (ansible.builtin.include_tasks) - Conditional
- **Phase 7: Deep cleanup** (ansible.builtin.include_tasks) - Conditional
- **Phase 8: APT cleanup** (ansible.builtin.include_tasks) - Conditional
- **Phase 9: Verify binary restoration** (ansible.builtin.include_tasks) - Conditional
- **Phase 10: Generate post-Ansible cleanup script** (ansible.builtin.include_tasks) - Conditional
- **Display cleanup summary** (ansible.builtin.debug) - Conditional
- **Cleanup skipped** (ansible.builtin.debug) - Conditional

### optimize_binaries.yml


- **Backup binaries before optimization** (ansible.builtin.copy)
- **Strip debug symbols from binaries** (ansible.builtin.command)
- **Compress binaries with UPX (if available)** (ansible.builtin.command) - Conditional
- **Test binaries after optimization** (ansible.builtin.command)
- **Restore binaries if optimization broke them** (ansible.builtin.copy) - Conditional
- **Remove binary backups** (ansible.builtin.file)
- **Ensure binary permissions are correct** (ansible.builtin.file)
- **Display optimization summary** (ansible.builtin.debug)

### protect_packages.yml


- **Protect packages from autoremoval (Debian family)** (ansible.builtin.command) - Conditional
- **Display protected packages** (ansible.builtin.debug) - Conditional

### remove_artifacts.yml


- **Remove source directories from install path** (ansible.builtin.file) - Conditional
- **Remove specified cleanup paths** (ansible.builtin.file) - Conditional
- **Remove additional cleanup paths** (ansible.builtin.file) - Conditional
- **Remove common build artifacts from user home** (ansible.builtin.file)
- **Remove common build artifacts from root** (ansible.builtin.file)
- **Display artifact removal summary** (ansible.builtin.debug)

### remove_dev_packages.yml


- **Remove development packages (Debian family)** (ansible.builtin.apt) - Conditional
- **Remove development packages (RedHat family)** (ansible.builtin.dnf) - Conditional
- **Set fact that autoremove has been run** (ansible.builtin.set_fact) - Conditional
- **Display package removal summary** (ansible.builtin.debug)

### verify_restore.yml


- **Check if binaries exist** (ansible.builtin.stat)
- **Display missing binaries warning** (ansible.builtin.debug) - Conditional
- **Verify binary permissions** (ansible.builtin.file)
- **Test binary execution with version flag** (ansible.builtin.command)
- **Display binary test results** (ansible.builtin.debug)
- **Fail if any binary test failed** (ansible.builtin.fail) - Conditional
- **Create verification summary** (ansible.builtin.set_fact)
- **Display verification summary** (ansible.builtin.debug)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - build_cleanup
```

## Author Information

- **Author**: CowDogMoo
- **Company**: CowDogMoo
- **License**: MIT

## Platforms


- Ubuntu: focal, jammy, noble
- Debian: bullseye, bookworm
- EL: 8, 9
<!-- DOCSIBLE END -->
