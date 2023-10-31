#!/usr/bin/python3
# Author: Jayson Grace <jayson.e.grace@gmail.com>

from ansible.module_utils.basic import AnsibleModule
import json

DOCUMENTATION = r'''
---
module: vnc_pw
short_description: Manage VNC passwords for users.
description:
  - Generates or retrieves VNC passwords for a list of users.
options:
  vnc_zsh_users:
    description:
      - List of users to manage VNC passwords for.
    type: list
    required: True
'''

def run_module():
    module_args = dict(
        ls_dicts = dict(type='list', required=True),
        ls = dict(type='list', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ls_dicts = module.params['ls_dicts']
    ls = module.params['ls']

    for a, b in zip(ls_dicts, ls):
        a['uid'] = b

    module.exit_json(changed=False, result=ls_dicts)

def main():
    run_module()

if __name__ == '__main__':
    main()
