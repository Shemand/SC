from datetime import datetime

from flask import request

from ....sc_common.authenticate import read_token
from ..api_Response import MiddlewareResponse


class BlueprintAttacher():
    def __init__(self, mod, base_name):
        self.base_name = 'computers'
        self.base_path = f'/<district_name>/{base_name}'

        def path(route_path):
            if route_path == '/':
                return self.base_path
            else:
                if route_path[0] == '/':
                    return f'{self.base_path}{route_path}'
                else:
                    return f'{self.base_path}/{route_path}'

        def route(rule, **options):
            def decorator(func):
                def middleware_func(**kwargs):
                    if not 'district_name' in kwargs:
                        raise RuntimeError("Each response must have district_name")
                    res = MiddlewareResponse()
                    res.set_district(kwargs['district_name'])
                    if 'Authorization' in request.headers:
                        try:
                            res.set_user(read_token(request.headers['Authorization'])['user_id'])
                            res.set_auth(True)
                        except Exception:
                            res = res.error()
                            res.append_message("Error in authorization header")
                            return res.error().get()
                    else:
                        res.set_user(None)
                        res.set_auth(False)
                    del kwargs['district_name']
                    return func(res, **kwargs)
                print(f'{self.base_path}:{rule}:{path(rule)}')
                mod.add_url_rule(path(rule), str(datetime.now().microsecond), middleware_func, **options)
            return decorator


        self._attach(route)

    def _attach(self, route):
        raise RuntimeError('Method BlueprintAttacher._attach must be released.')
