import json

from sqlalchemy.sql.functions import user

from backend.sc_actions.units import get_unit_by_id, get_available_units_id
from backend.sc_actions.users import get_user_by_id
from backend.sc_entities.Entities import Entities


class ApiEntity():
    def __init__(self):
        pass

    def get(self):
        return {}


class EntityDistrict(ApiEntity):
    def __init__(self, district):
        super().__init__()
        self.district = district

    def get(self):
        return self.district.name


class EntityUser(ApiEntity):
    def __init__(self, user):
        super().__init__()
        self._user = user
        self.unit = None
        self.available_units = None

    @property
    def user_obj(self):
        return self._user

    def set_unit(self, database):
        self.unit = get_unit_by_id(database, self.user_obj.Units_id)

    def set_available_units(self, database):
        if self.unit is not None:
            self.available_units = get_available_units_id(database, self.unit.name)

    def get(self):
        return {
            "username" : self.user_obj.username,
            "full_name" : self.user_obj.full_name,
            "privileges" : self.user_obj.privileges
        }

    def __repr__(self):
        return json.dumps(self.get())


class ApiResponse:
    def __init__(self, district, user):
        self.district = EntityDistrict(district)
        self.user = EntityUser(user)
        self.messages = []
        self.data = None
        self.status_code = 200

    def append_message(self, message):
        self.messages.append(message)

    def get(self):
        return json.dumps({
            "district" : self.district.get(),
            "user" : self.user.get(),
            "messages" : self.messages,
            "data" : self.data
        }), self.status_code

class MiddlewareResponse():
    def __init__(self):
        self.user = None
        self.district = None
        self.auth = False

    def set_user(self, user_id):
        if not self.district:
            raise RuntimeError('For set user, necessary set district of user.')
        if user_id == None:
            self.user = None
        else:
            self.user = get_user_by_id(self.district.database, user_id)

    def set_district(self, district_name):
        self.district = Entities().get_district(district_name)

    def set_auth(self, value):
        self.auth = bool(value)

    def success(self, data={}):
        return SuccessApiResponse(self.district, self.user, data)

    def undefined(self):
        return UndefinedApiResponse()

    def error(self):
        return ErrorApiResponse(self.district, self.user)

    def unauth(self):
        return UnauthApiResponse()

    def denied(self):
        return PermissionApiResponse()

class SuccessApiResponse(ApiResponse):
    def __init__(self, district, user, data):
        super().__init__(district, user)
        self.data = data
        self.status_code = 200


class UndefinedApiResponse(ApiResponse):
    def __init__(self):
        super().__init__(None, None)
        self.status_code = 404


class ErrorApiResponse(ApiResponse):
    def __init__(self, district, user):
        super().__init__(district, user)
        self.status_code = 500


class UnauthApiResponse(ApiResponse):
    def __init__(self):
        super().__init__(None, None)
        self.status_code = 401


class PermissionApiResponse(ApiResponse):
    def __init__(self):
        super().__init__(None, None)
        self.status_code = 304
