import json

from flask import jsonify
from sqlalchemy.sql.functions import user


from ..sc_common.authenticate import read_token
from ..sc_entities.District import District
from ..sc_entities.Entities import Entities

_AUTH_TYPE = 0
_AUTH_TOKEN = 1


class MiddlewareResponse(): #todo from this
    def __init__(self, headers, json_body):
    # request data
        auth_data = self.__extract_auth(headers)
        self.json_body = json_body
        self.sc = self._get_service_controller()
        self.user = self._get_user(auth_data)
    # response data
        self.status_code = None
        self.messages = []
        self.data = {}

    def _get_database(self):
        # rc = RepositoryController()
        return rc.database

    def __extract_auth(self, headers):
        auth_data = {}
        if not 'Authorization' in headers:
            return auth_data
        auth = headers['Authorization']
        auth = auth.split(' ')
        auth_type = auth[_AUTH_TYPE]
        auth_token = auth[_AUTH_TOKEN]
        if auth_type == 'Bearer':
            auth_data = read_token(auth_token)
        return auth_data

    def _get_user(self, auth_data):
        if not auth_data:
            return None
        else:
            if 'user_name' in auth_data:
                return self.database.get_user(auth_data['user_name'])
            else:
                print('auth token without user_id')
                return None

    @property
    def loggined(self):
        if self.user:
            return True
        return False

    def set_data(self, key, value):
        self.data[key] = value

    def append_message(self, message):
        self.messages.append(message)

    def success(self):
        self.status_code = 200
        return self

    def undefined(self):
        self.status_code = 404
        return self

    def error(self, message=None):
        self.status_code = 500
        return self

    def unauth(self):
        self.status_code = 401
        return self

    def denied(self):
        self.status_code = 304
        return self

    def get(self):
        return jsonify({
            "district" : self.district.name,
            "user" : self.user.get(),
            "messages" : self.messages,
            "data" : self.data
        }), self.status_code