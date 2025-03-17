#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, annotations, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: realm_manage
short_decription: Interact with the realmd program
description:
    - This module manages realm membership on Linux systems.
    - This module passes its parameters to the realmd C(realm) command.
    - For configuring realm ACLs using V(permit) and V(deny), please see M(realm_acl).
author:
    - Christopher Harcourt (@themoosefulcorp)
version_added: "2.16.3"
options:
    action:
        aliases: [ state ]
        description:
            - Sub command to pass to the C(realm) command.
            - If V(discover), C(realm) will discover a realm and its capabilities. If no realm is specified, C(realm) will use the domain assigned through DHCP.
            - If V(list), C(realm) will list all of the discovered and configured realms.
            - If V(join), the system will be joined to the configured Kerberos realm using C(realm join).
            - If V(leave), the system will be removed from any existing Kerberos realms using C(realm leave).
        type: str
        required: true
        choices: [ discover, list, join, leave ]
    client_software:
        description:
            - Which client software the realm uses.
            - If O(action=discover), C(realm) will only return realms using the specified client software.
        type: str
        choices: [ sssd, winbind ]
    computer_name:
        description:
            - What name to use when creating the computer account.
            - Requires a string of 15 or fewer characters that is a valid NetBIOS name.
            - Used when O(server_software=active-directory).
        type: str
    computer_ou:
        description:
            - The distinguished name of the OU in which to create the computer account.
            - Typically, you can omit the root DSE portion.
            - Used when O(server_software=active-directory).
        type: str
    discover_all:
        description:
            - TODO replace with show_all
            - Whether or not C(realm discover) should show all discovered realms.
            - Requires O(action=discover).
        type: bool
    discover_name:
        description:
            - TODO replace with name_only
            - Whether or not C(realm discover) should return only the names of the discovered realms.
            - Requires O(action=discover).
        type: bool
    list_all:
        description:
            - TODO replace with show_all
            - Whether or not C(realm list) should show all discovered realms.
            - Requires O(action=list).
        type: bool
    list_name:
        description:
            - TODO replace with name_only
            - Whether or not C(realm list) should return only the names of the discovered realms.
            - Requires O(action=list).
        type: bool
    membership_software:
        description:
            - Which membership software the realm uses.
            - If O(action=discover), C(realm) will only return realms using the specified server software.
        type: str
        choices: [ adcli, samba ]
    name_only:
        description:
            - Placeholder
        type: bool
    no_password:
        description:
            - Used with O(action=join).
            - Attempt to perform the C(realm join) without a password.
            - Mutually exclusive with O(one_time_password) and O(password).
        type: bool
    one_time_password:
        description:
            - Used with O(action=join).
            - Perform C(realm join) with a one-time password.
            - Not possible with all types of realms.
            - Mutually exclusive with O(no_password) and O(password).
        type: str
    os_name:
        description:
            -
        type: str
    os_version:
        description:
            -
        type: str
    password:
        description:
            - Plain-text password of the supplied domain account.
            - Mutually exclusive with O(one_time_password) and O(no_password).
        type: str
    server_software:
        description:
            - Which server software the realm uses.
            - If O(action=discover), C(realm) will only return realms using the specified server software.
        type: str
        choices: [ active-directory, ipa ]
    show_all:
        description:
            - Placeholder
        type: bool
    use_ldaps:
        description:
            - Whether or not C(realm) should force a connection over LDAPS when connecting to AD.
            - This option is only needed if the standard LDAP port (389/tcp) is unavailable.
            - Will only be applied when O(server_software=active-directory) and O(membership_software=adcli) are specified.
        type: bool
        default: false
    user:
        description:
            -
        type: str
...
"""


import os
from ansible.module_utils.basic import AnsibleModule


def discover(discover_all, client_software, discover_name, membership_software, server_software, use_ldaps):
    flags = []
    if discover_all:
        flags.append('--all')
    if client_software:
        flags.extend(['--client-software', client_software])
    if discover_name:
        flags.append('--name')
    if membership_software:
        flags.extend(['--membership-software', membership_software])
    if server_software:
        flags.extend(['--server-software', server_software])
    if use_ldaps:
        flags.append('--use-ldaps')
    return flags


def list(list_all, list_name):
    flags = []
    if list_all:
        flags.append('--all')
    if list_name:
        flags.append('--name-only')
    return flags


def join(client_software, computer_name, computer_ou, membership_software, no_password, one_time_password, os_name, os_version, server_software, use_ldaps, user):
    flags = []
    if client_software:
        flags.extend(['--client-software', client_software])
    if computer_name:
        flags.extend('--computer-name', computer_name)
    if computer_ou:
        flags.extend('--computer-ou', computer_ou)
    if membership_software:
        flags.extend(['--membership-software', membership_software])
    if no_password:
        flags.append('--no-password')
    if one_time_password:
        flags.extend('--one-time-password', one_time_password)
    if os_name:
        flags.extend('--os-name', os_name)
    if os_version:
        flags.extend('--os-version', os_version)
    if server_software:
        flags.extend(['--server-software', server_software])
    if use_ldaps:
        flags.append('--use-ldaps')
    if user:
        flags.extend('--user', user)
    return flags


def leave(client_software, remove, server_software, use_ldaps, user):
    flags = []
    if client_software:
        flags.extend(['--client-software', client_software])
    if remove:
        flags.append('--remove')
    if server_software:
        flags.extend(['--server-software', server_software])
    if use_ldaps:
        flags.append('--use-ldaps')
    if user:
        flags.extend(['--user', user])
    return flags


def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(aliases=['state'], type='str', required=True, choices=['discover', 'list', 'join', 'leave']),
            client_software=dict(type='str', choices=['sssd', 'winbind']),
            computer_name=dict(type='str'),
            computer_ou=dict(type='str'),
            discover_all=dict(type='bool'),
            discover_name=dict(type='bool'),
            list_all=dict(type='bool'),
            list_name=dict(type='bool'),
            membership_software=dict(type='str', choices=['acli', 'samba']),
            no_password=dict(type='bool'),
            one_time_password=dict(type='str', no_log=True),
            os_name=dict(type='str'),
            os_version=dict(type='str'),
            password=dict(type='str', no_log=True),
            realm=dict(type='str'),
            remove=dict(type='bool'),
            server_software=dict(type='str', choices=['active-directory','ipa']),
            use_ldaps=dict(type='bool', default=False),
            user=dict(type='str')
        ),
        supports_check_mode=False,
        required_together=(
            [['action', 'discover'], 'discover_all'],
            [['action', 'discover'], 'discover_name'],
            [['action', 'list'], 'list_all'],
            [['action', 'list'], 'list_name']
        ),
        required_if=(
            ['use_ldaps', True, ['membership_software', 'server_software']],
            ['remove', True, ['user', 'password']]
        ),
        required_by={
            'password': 'user'
        },
        mutually_exclusive=(
            ['no_password', 'one_time_password', 'password']
        )
    )

    action = module.params['action']
    client_software = module.params['client_software']
    computer_name = module.params['computer_name']
    computer_ou = module.params['computer_ou']
    discover_all = module.params['discover_all']
    discover_name = module.params['discover_name']
    list_all = module.params['list_all']
    list_name = module.params['list_name']
    membership_software = module.params['membership_software']
    no_password = module.params['no_password']
    one_time_password = module.params['one_time_password']
    os_name = module.params['os_name']
    os_version = module.params['os_version']
    password = module.params['password']
    realm = module.params['realm']
    remove = module.params['remove']
    server_software = module.params['server_software']
    use_ldaps = module.params['use_ldaps']
    user = module.params['user']
   
    match action:
        case "discover":
            args = discover(discover_all, client_software, discover_name, membership_software, server_software, use_ldaps)
        case "list":
            args = list(list_all, list_name)
        case "join":
            args = join(client_software, computer_name, computer_ou, membership_software, no_password, one_time_password, os_name, os_version, server_software, use_ldaps, user)
        case "leave":
            args = leave(client_software, remove, server_software, use_ldaps, user)

    binary = module.get_bin_path('realm', required=True)
    command = [ binary, action, '--unattended' ]
    command.append(args)
    
    if realm:
        command.append(realm)

    rc, stdout, stderr = module.run_command(args=command, data=password)
    results = dict(rc=rc, stdout=stdout, stderr=stderr)

    if results['rc'] != 0:
        module.fail_json(msg='Failed to run {0}: {1}'.format(args, stderr), **results)
    else:
        module.exit_json(changed=True, **results)


if __name__ == '__main__':
    main()