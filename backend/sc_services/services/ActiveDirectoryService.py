from datetime import datetime
from typing import Any, List

import ldap3
from ldap3 import Connection, Server, AUTO_BIND_NO_TLS, SUBTREE

from backend.sc_common.functions import reformat_computer_name, transformate_time
from backend.sc_services.services.ServiceAbstract import ServiceAbstract


class ActiveDirectoryService(ServiceAbstract):

    _catalog_path: str
    _begin_node: str
    _end_nodes: [str]

    def __init__(self, configurations: dict) -> None:
        super().__init__(configurations['name'], configurations)
        self._catalog_path = configurations['path']
        self._begin_node = configurations['begin_node']
        self._end_nodes = configurations['end_nodes']
        self._server = Server(self.configuration['ip'],
                              port=self.configuration['port'],
                              use_ssl=False)

    def create_connection(self) -> Any:
        print('connection create')
        self._connection = Connection(self._server,
                                      auto_bind=AUTO_BIND_NO_TLS,
                                      user=self.configuration['username'],
                                      password=self.configuration['password'])
        if self._connection:
            return self._connection
        else:
            assert 'Could create new connection for Active Directory (' + self._name + ')'
            return None

    def check_connection(self) -> bool:
        pass

# Computers manipulations

    def _get_computers_raw(self, size_limit=0):
        self.connection.search(search_base=self._catalog_path,
                               search_filter='(objectClass=computer)',
                               search_scope=SUBTREE,
                               attributes=["name", "distinguishedName", "lastLogonTimestamp",
                                           "objectGUID", "objectSid", "sAMAccountName",
                                           "userAccountControl", "whenCreated"],
                               size_limit=size_limit)
        return self.connection.response

    def get_computers(self):
        raw_data = self._get_computers_raw()
        computers = [ {
            "name": reformat_computer_name(record['attributes']['name']),
            "dn": [ list(reversed(dn.split('=')))[0] for dn in reversed(record['attributes']['distinguishedName'].split(',')) ],
            "last_logon": transformate_time(record['attributes']['lastLogonTimestamp']),
            "GUID": record['attributes']['objectGUID'],
            "SID": record['attributes']['objectSid'],
            "user_account_control": record['attributes']['userAccountControl'],
            "locked" : record['attributes']['userAccountControl'] & 0x10,
            "disabled" : record['attributes']['userAccountControl'] & 0x2,
            "whenCreated": transformate_time(record['attributes']['whenCreated']),
        } for record in raw_data]
        return computers

# Users manipulations

    def _get_users_raw(self, size_limit=0):
        self.connection.search(search_base=self._catalog_path,
                               search_filter=' (sAMAccountType=805306368)', # or (&(objectCategory=person)(objectClass=user))
                               search_scope=SUBTREE,
                               attributes=["name", "distinguishedName", "badPasswordTime",
                                           "lastLogonTimestamp", "mail", "mailNickname",
                                           "objectGUID", "objectSid", "sAMAccountName",
                                           "telephoneNumber", "targetAddress", "userAccountControl",
                                           "whenCreated", "department"],
                               size_limit=size_limit)
        return self.connection.response

    def get_users(self):
        raw_data = self._get_users_raw()
        users = [ {
            "name": reformat_computer_name(record['attributes']['name']),
            "dn": [ list(reversed(dn.split('=')))[0] for dn in reversed(record['attributes']['distinguishedName'].split(',')) ],
            "last_logon": transformate_time(record['attributes']['lastLogonTimestamp']),
            "bad_password_time" : transformate_time(record['attributes']['badPasswordTime']),
            "mail" : record['attributes']['mail'] if 'mail' in record['attributes'] else None,
            "phone" : record['attributes']['telephoneNumber'] if 'telephoneNumber' in record['attributes'] else None,
            "address" : record['attributes']['targetAddress'] if 'targetAddress' in record['attributes'] else None,
            "department" : record['attributes']['department'] if 'department' in record['attributes'] else None,
            "GUID": record['attributes']['objectGUID'] if 'objectGUID' in record['attributes'] else None,
            "SID": record['attributes']['objectSid'] if 'objectSid' in record['attributes'] else None,
            "user_account_control": record['attributes']['userAccountControl']
                                    if 'userAccountControl' in record['attributes']
                                    else None,
            "locked" : record['attributes']['userAccountControl'] & 0x10,
            "disabled" : record['attributes']['userAccountControl'] & 0x2,
            "whenCreated": transformate_time(record['attributes']['whenCreated']),
        } for record in raw_data]
        return users

# Location manupulation

    def _get_containers_raw(self, size_limit=0):
        self.connection.search(search_base=self._catalog_path,
                               search_filter='(objectCategory=organizationalUnit)',
                               search_scope=SUBTREE,
                               attributes=["*"],
                               size_limit=size_limit)
        return self.connection.response

    def get_locations_tree(self):
        raw_data = self._get_containers_raw()
        locations_tree = {}
        containers = [ (record['attributes']['name'],
                        record['attributes']['objectGUID'],
                        [ list(reversed(node.split('=')))[0]
                          for node in list(reversed(record['attributes']['distinguishedName'].split(',')))]
                        ) for record in raw_data
                     ]
        for container in containers:
            name, guid, path = container
            while path[0] != self._begin_node:
                path.pop(0)
            self._recursive_build(locations_tree, path)
        return locations_tree

    def _recursive_build(self, sub_tree, nodes):
        node = nodes.pop(0).strip()
        if node not in sub_tree:
            sub_tree[node] = {}
        if node in self._end_nodes:
            return
        if len(nodes) > 0:
            self._recursive_build(sub_tree[node], nodes)

    def authenticate_user(self, login: str, password: str) -> bool:
        c = Connection(self._server, user=login, password=password)
        if not c.bind():
            return False
        return True