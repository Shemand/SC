import base64
import ipaddress
from datetime import datetime
from time import sleep

import requests
import urllib3
from requests import ReadTimeout, ConnectTimeout, Session
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError, NewConnectionError
import json

from ..sc_common.functions import reformat_computer_name
from .ServiceAbstract import ServiceAbstract


class KasperskyService(ServiceAbstract):
    URLS = {
        "create_connection": "api/v1.0/login",
        "get_groups": "api/v1.0/HostGroup.FindGroups",
        "get_hosts": "api/v1.0/HostGroup.FindHosts",
        "get_chunks": "api/v1.0/ChunkAccessor.GetItemsChunk",
        "get_count": "api/v1.0/ChunkAccessor.GetItemsCount",
        "get_AdGroups": "api/v1.0/VServers.GetVServers",
        "get_host_products": "api/v1.0/HostGroup.GetHostProducts",
        "get_host_info": "api/v1.0/HostGroup.GetHostInfo",
        "get_static_info": "api/v1.0/HostGroup.GetStaticInfo",
        "get_child_servers": "api/v1.0/ServerHierarchy.GetChildServers",
        "get_find_slave_servers": "api/v1.0/ServerHierarchy.FindSlaveServers",
        "get_async_hosts": "api/v1.0/HostGroup.FindHostsAsync",
        "chunk_release": "api/v1.0/ChunkAccessor.Release",
        "get_async_status": "api/v1.0/AsyncActionStateChecker.CheckActionState",
        "get_async_accessor": "api/v1.0/HostGroup.FindHostsAsyncGetAccessor",
        "add_host": "api/v1.0/HostGroup.AddHost",
        "update_host": "api/v1.0/HostGroup.UpdateHost"
    }

    def get_url(self, url):
        return f'https://{self.ip}:{self.port}/{KasperskyService.URLS[url]}'

    def __init__(self, district, main_config, specific_data) -> None:
        super().__init__(district, main_config, specific_data)
        self.session = None
        self.server = self.configuration['server']
        self.username = self.configuration['username']
        self.username = base64.b64encode(self.username.encode("UTF-8")).decode("UTF-8")
        self.password = self.configuration['password']
        self.password = base64.b64encode(self.password.encode("UTF-8")).decode("UTF-8")
        self.auth_headers = {"Authorization": 'KSCBasic user="' + self.username + '", pass="' + self.password + '"',
                             "Content-Type": "application/json",
                             "Content-Length": "2"}
        self.common_headers = {"Content-Type": "application/json"}

    def _tune_session(self):
        session = Session()
        adapter = HTTPAdapter(pool_maxsize=100, pool_connections=100)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers = self.common_headers
        return session

    def check_connection(self) -> bool:
        if not self.session:
            self.create_connection()
        if self.session:
            return True
        return False

    def create_connection(self):
        self.session = self._tune_session()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            response = self.session.post(url=self.get_url('create_connection'), headers=self.auth_headers, data="{}",
                                         verify=False, timeout=30)
            if response.status_code == 401:
                print(
                    "[ERROR] (" + self._name + ") Authentication required. Check the policies or privileges of account!")
                return None
        except ReadTimeout:
            print('ReadTimeout')
            print("thread of connection to " + self._name + " ended with timeout")
            return None
        except ConnectTimeout:
            print('ConnectTimeout')
            print("thread of connection to " + self.get_url(
                'create_connection') + " (" + self._name + ") ended with max retries exceeded (perhaps no privileges)")
            return None
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            print("thread of connection to " + self.get_url(
                'create_connection') + " (" + self._name + ") ended with max retries exceeded (perhaps no privileges)")
            return None
        except MaxRetryError:
            print('MaxRetryError')
            print(
                "thread of connection to 'create_connection' " + self._name + " ended with max retries exceeded (perhaps no privileges)")
            return None
        except NewConnectionError as Err:
            if Err.errno == 113:
                print(
                    "thread of connection to 'create_connection' " + self._name + " ended with error 'No route to host'")
            else:
                print("While connection to 'create_connection' with error 'NewConnectionError' (errno not a 113)")
            return None
        print("connection created: " + self._name + " - status is - " + str(response.status_code))
        return response.status_code

    def _get_computers_raw(self):
        request_key = self.__send_async_request()
        finalized = False
        succeded_finalized = False
        while not finalized and not succeded_finalized:
            sleep(2)
            succeded_finalized, finalized = self.__check_request_state(request_key)
            if succeded_finalized:
                accessor = self.__get_accessor(request_key)
                count = self.__item_count_by_accesor(accessor)
                data = self.__get_chunks(accessor, count)
                self.__release_accessor(accessor)
                data = [row['value'] for row in data]
                data = [{key: (row[key]['value'] if isinstance(row[key], dict) and 'value' in row[key] else row[key]) for key in row} for row in data]
                return data
        return None

    def get_computers(self):
        self.__records = {}
        self.__records = self._get_computers_raw()
        data = {}
        for record in self.__records:
            name = reformat_computer_name(record["KLHST_WKS_DN"])
            info = {
                "name" : name,
                "server": self.server,
                "hasDuplicate": False,
                "os": record["KLHST_WKS_OS_NAME"] if "KLHST_WKS_OS_NAME" in record else None,
                "ip": str(ipaddress.ip_address(record['KLHST_WKS_IP_LONG'])) if "KLHST_WKS_IP_LONG" in record else None,
                "last_visible": datetime.strptime(str(record["KLHST_WKS_LAST_VISIBLE"]), "%Y-%m-%dT%H:%M:%SZ")
                                 if "KLHST_WKS_LAST_VISIBLE" in record else None,
                "created": datetime.strptime(str(record["KLHST_WKS_CREATED"]), "%Y-%m-%dT%H:%M:%SZ")
                            if "KLHST_WKS_CREATED" in record else None,
                "agent_version": record["KLHST_WKS_NAG_VERSION"] if "KLHST_WKS_NAG_VERSION" in record else None,
                "security_version": record["KLHST_WKS_RTP_AV_VERSION"] if "KLHST_WKS_RTP_AV_VERSION" in record else None,
                "virus": record["KLHST_WKS_VIRUS_COUNT"] if "KLHST_WKS_VIRUS_COUNT" in record else None,
                "dns_name": record['KLHST_WKS_DNSNAME'] if "KLHST_WKS_DNSNAME" in record else None,
                "started": datetime.strptime(str(record["KLHST_WKS_LAST_SYSTEM_START"]),"%Y-%m-%dT%H:%M:%SZ")
                            if "KLHST_WKS_LAST_SYSTEM_START" in record else None
            }
            if not name in data:
                data[name] = info
            else:
                data[name] = self._compare_duplicates(data[name], info)
        return data

    def _compare_duplicates(self, current_record, new_record):
        current_visible = current_record['last_visible']
        new_visible = new_record['last_visible']
        if current_visible and new_visible and current_visible < new_visible:
            return new_record
        elif not current_visible and new_visible:
            return current_record
        elif not current_visible and not new_visible:
            return None

    def __send_async_request(self):
        data = self.__prepare_request_body()
        response = self.session.post(url=self.get_url('get_async_hosts'),
                                     headers=self.common_headers, data=data, verify=False)
        print(response)
        key = json.loads(response.content)['strRequestId']
        return key

    def __prepare_request_body(self):
        body = {
            "wstrFilter": "(&(KLHST_WKS_FROM_UNASSIGNED=0)(KLHST_WKS_STATUS & 4<>0))",
            "vecFieldsToReturn": ["KLHST_WKS_OS_NAME",
                                  "KLHST_WKS_IP_LONG",
                                  "KLHST_WKS_DN",
                                  "KLHST_WKS_LAST_VISIBLE",
                                  "KLHST_WKS_CREATED",
                                  "KLHST_WKS_NAG_VERSION",
                                  "KLHST_WKS_RTP_AV_VERSION",
                                  "KLHST_WKS_VIRUS_COUNT",
                                  "KLHST_WKS_LAST_SYSTEM_START",
                                  "KLHST_WKS_DNSNAME"],
            "pParams": {"KLSRVH_SLAVE_REC_DEPTH": 0, "KLGRP_FIND_FROM_CUR_VS_ONLY": False},
            "lMaxLifeTime": 100
        }
        return json.dumps(body)

    def __check_request_state(self, key):
        data = {
            "wstrActionGuid": str(key)
        }
        data = json.dumps(data)
        response = self.session.post(
            url=self.get_url('get_async_status'),
            headers=self.common_headers, data=data, verify=False)
        response = json.loads(response.content)
        return response['bSuccededFinalized'], response['bFinalized']

    def __get_accessor(self, str_request_id: str):
        data = {
            "strRequestId": str(str_request_id)
        }
        data = json.dumps(data)
        response = self.session.post(
            url=self.get_url('get_async_accessor'),
            headers=self.common_headers, data=data, verify=False)
        return json.loads(response.content)['strAccessor']

    def __item_count_by_accesor(self, accessor):
        data = {
            "strAccessor": accessor
        }
        data = json.dumps(data)
        response = self.session.post(
            url=self.get_url('get_count'),
            headers=self.common_headers, data=data, verify=False)
        return json.loads(response.content)["PxgRetVal"]

    def __get_chunks(self, accessor, count, step=10000):
        start = 0
        data = {
            "strAccessor": accessor,
            "nStart": start,
            "nCount": step
        }
        data = json.dumps(data)
        response = self.session.post(
            url=self.get_url('get_chunks'),
            headers=self.common_headers, data=data, verify=False)
        data = json.loads(response.content)
        data = data['pChunk']['KLCSP_ITERATOR_ARRAY']
        return data

    def __release_accessor(self, accessor):
        data = {
            "strAccessor": accessor
        }
        data = json.dumps(data)
        response = self.session.post(
            url=self.get_url('chunk_release'),
            headers=self.common_headers, data=data, verify=False)
