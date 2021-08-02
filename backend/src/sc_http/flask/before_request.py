from flask import g, request

from ....sc_common.authenticate import read_token
from ..api_Response import MiddlewareResponse

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
    if auth_type == 'Bearer':
        auth_data = read_token(auth_token)
    return auth_data


def attach_before_request(app):
    @app.before_request
    def before_req():
        token_data = __extract_token(request)
        if 'user_id' in token_data:
            g.middleware = MiddlewareResponse(token_data['user_id'])
        else:
            g.middleware = MiddlewareResponse(None)
