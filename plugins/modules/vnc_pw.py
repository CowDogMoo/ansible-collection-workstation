#!/usr/bin/python3
# Author: Jayson Grace <jayson.e.grace@gmail.com>

from ansible.module_utils.basic import AnsibleModule
import json
import os
import secrets
import string
import subprocess

def file_exists(file):
    if os.path.isfile(file):
        return True
    else:
        return False

def gen_pw(size):
    return ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(size)))

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

def run_module():
    module_args = dict(
	vnc_zsh_users = dict(type='list', required=True),
    )

    module = AnsibleModule(
	argument_spec=module_args,
	supports_check_mode=True
    )

    vnc_users = module.params['vnc_zsh_users']

    for user in vnc_users:
        if not file_exists(f"/home/{user['username']}/.vnc/passwd"):
            user['pass'] = gen_pw(8)
        else:
            command = f"vncpwd /home/{user['username']}/.vnc/passwd"
            user['pass'] = run_cmd(command).strip().decode('utf-8').split()[1]

    module.exit_json(changed=False, result=vnc_users)

def main():
    run_module()

if __name__ == '__main__':
    main()
