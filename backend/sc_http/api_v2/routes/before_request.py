from flask import g, request

from backend.sc_common.authenticate import read_token
from backend.sc_http.api_v2.api_Response import MiddlewareResponse

_DISTRICT_NAME = 0
_GROUP_NAME = 1

_AUTH_TYPE = 0
_AUTH_TOKEN = 1


def __split_and_extract_path(path, mod_path):
    real_path_index = path.find(mod_path)
    if real_path_index == -1:
       return None
    path = path[real_path_index + len(mod_path):]
    return path.split('/')


def __extract_token(request):
    auth_data = {}
    if not 'Authorization' in request.headers:
        return auth_data
    auth = request.headers['Authorization']
    auth = auth.split(' ')
    auth_type = auth[_AUTH_TYPE]
    auth_token = auth[_AUTH_TOKEN]
    if auth_type == 'jwt':
        auth_data = read_token(auth_token)
    return auth_data


def attach_before_request(mod, mod_path):
    @mod.before_request
    def before_req():
        path = __split_and_extract_path(request.path, mod_path)
        if path is None:
            return g.response.error(message='unknown path of mod').get()
        if len(path) < 2:
            return g.response.error(message='response must have district and group. Example: "/api/v1/SZO/computers"').get()
        token_data = __extract_token(request)
        if 'user_id' in token_data:
            g.response = MiddlewareResponse(path[_DISTRICT_NAME], path[_GROUP_NAME], token_data['user_id'])
        else:
            g.response = MiddlewareResponse(path[_DISTRICT_NAME], path[_GROUP_NAME], None)
