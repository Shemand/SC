import json

from flask import g, request

from backend.sc_actions.active_directory import get_ad_user
from backend.sc_actions.users import get_user, add_user
from backend.sc_common.authenticate import generate_token
from .BlueprintAttacher import BlueprintAttacher


def attach_user_rotes(mod):
    @mod.route('/<district_name>/users/role', methods=['GET'])
    def get_user_role(district_name):
        '''Function for getting information about computers in districts according'''
        res = g.response
        for service in res.district.services.get_active_directory_services():
            service.create_connection()
            x = service.get_users()
            print('ff')
        return '{}'

    @mod.route('/<district_name>/users/auth', methods=['POST'])
    def authenticate(district_name):
        res = g.response
        data = json.loads(request.data)
        if isinstance(data, dict)\
            and 'login' in data\
            and 'password' in data:
            if res.district.services.authenticate_user(data['login'], data['password']):
                user = get_user(res.database, data['login'])
                if not user:
                    user = add_user(data['login'], get_ad_user(g.response.database, data['login']))
                    g.response.database.session.commit()
                res.success()
                res.set_data('jwt_token', generate_token(user.id))
                return res.get()
        return res.unauth().get()

    @mod.route('/<district_name>/users/registration', methods=['POST'])
    def registration(district_name):
        return '{}'
