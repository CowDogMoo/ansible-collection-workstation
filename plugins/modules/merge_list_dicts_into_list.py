#!/usr/bin/python3
# Author: Jayson Grace <jayson.e.grace@gmail.com>

from ansible.module_utils.basic import AnsibleModule
import json

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
