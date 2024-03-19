#!/usr/bin/env python

import sys
import pwd
import operator
from json import dumps

def getent():
    all_users = pwd.getpwall()
    users = {user.pw_name: ["x", user.pw_uid, user.pw_gid, user.pw_gecos, user.pw_dir, user.pw_shell] for user in all_users}
    return users

def main():
    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True
    )

    try:
        users = getent()
        module.exit_json(changed=False, ansible_facts={'getent_passwd': users})
    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
