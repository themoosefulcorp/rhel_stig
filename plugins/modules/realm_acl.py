#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, annotations, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: realm_acl
short_decription: Interact with realmd ACLs
description:
    - This module manages realm user access on Linux systems.
    - This module passes its parameters to the realmd C(realm permit) or C(realm deny) commands.
    - For managing realm membership, please see M(realm_manage).
author:
    - Christopher Harcourt (@themoosefulcorp)
options:
    scope:
        type: str
        default: 'all'
    state:
        description:
            - Sub command to pass to the C(realm) command.
            - C(realm) will configure local login by realm users according to the passed value.
        type: str
        required: true
        choices: [ permit, deny ]
...
"""

import os
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=value
        )
    )

if __name__ == '__main__':
    main()