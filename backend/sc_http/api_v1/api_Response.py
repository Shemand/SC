import json

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
        return {}


class EntityUser(ApiEntity):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def get(self):
        return {}


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
        return self.status_code, json.dumps({
            "district" : self.district.get(),
            "user" : self.district.get(),
            "messages" : self.messages,
            "data" : self.data
        })

class MiddlewareResponse():
    def __init__(self):
        self.user = None
        self.district = None

    def set_user(self, user_id):
        if not self.district:
            raise RuntimeError('For set user, necessary set district of user.')
        self.user = user

    def set_district(self, district_name):
        self.district = Entities().get_district(district_name)

    def success(self, data):
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
