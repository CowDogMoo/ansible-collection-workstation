#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import os
import secrets
import string
import subprocess

DOCUMENTATION = r'''
---
module: vnc_pw
short_description: Manage VNC passwords for users.
description:
  - Generates or retrieves VNC passwords for a list of users.
options:
  vnc_users:
    description:
      - List of users to manage VNC passwords for.
    type: list
    required: True
'''

def file_exists(file):
    return os.path.isfile(file)

def gen_pw(size):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(size))

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()
    return output

def get_home_dir(username):
    return '/root' if username == 'root' else f"/home/{username}"

def run_module():
    module_args = dict(
        vnc_users=dict(type='list', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    vnc_users = module.params['vnc_users']

    for user in vnc_users:
        home_dir = get_home_dir(user['username'])
        passwd_file = f"{home_dir}/.vnc/passwd"
        
        if not file_exists(passwd_file):
            user['pass'] = gen_pw(8)
        else:
            command = f"vncpwd {passwd_file}"
            user['pass'] = run_cmd(command).strip().decode('utf-8').split()[1]

    module.exit_json(changed=False, result=vnc_users)

def main():
    run_module()

if __name__ == '__main__':
    main()
