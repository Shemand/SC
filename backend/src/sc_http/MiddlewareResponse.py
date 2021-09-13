import json

from flask import jsonify
from sqlalchemy.sql.functions import user


from ..sc_common.authenticate import read_token
from ..sc_repositories.DatabaseModels.UsersTable import UsersTable
from ..sc_entities.District import District
from ..sc_entities.Entities import Entities


class EntityUser():
    def __init__(self, district: District, user_id):
        super().__init__()
        if not isinstance(district, District):
            raise TypeError('EntityUser.__init__: wrong district type')
        self.district = district
        self.database = self.district.database
        self._set_user(user_id)
        self.unit = None
        self.available_units = []
        if self._user:
            self._set_unit()
            self._set_available_units()

    @property
    def user_obj(self):
        return self._user

    @property
    def empty(self):
        if self._user:
            return False
        return True

    def _set_user(self, user_id):
        if user_id is None:
            self._user = None
            return
        user = self.database.session.query(UsersTable).filter_by(id=user_id).first()
        if user:
            self._user = user
        else:
            raise RuntimeError('Unknown user_id')

    def _set_unit(self):
        self.unit = get_unit_by_id(self.database, self.user_obj.Units_id)

    def _set_available_units(self):
        if self.unit is not None:
            self.available_units = get_available_units_id(self.database, self.unit.name)

    def get(self):
        if not self.empty:
            return {
                "username": self._user.login,
                "privileges": self._user.privileges
            }
        return None

    def __repr__(self):
        return json.dumps(self.get())


class MiddlewareResponse(): #todo from this
    def __init__(self, user_id, body):
    # request data
        self.district = None
        self.group_name = None
        self.user = None
        self.loggined = False
        self.database = None
        self._set_district('SZO') # todo remove this
        self._set_route_group('computers') # todo remove this
        self._set_user(user_id)
        self.body = body
    # response data
        self.status_code = None
        self.messages = []
        self.data = {}

    def _set_user(self, user_id):
        if not self.district:
            raise RuntimeError('For set user, necessary set district of user.')
        self.user = EntityUser(self.district, user_id)
        if self.user.empty:
            self.loggined = False
        else:
            self.loggined = True

    def _set_district(self, district_name):
        self.district = Entities().get_district(district_name)
        self.database = self.district.database

    def _set_route_group(self, group_name):
        self.group_name = group_name

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