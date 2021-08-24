import json

from flask import g, request

from ...sc_services.ActiveDirectoryService import get_ad_user, get_ad_users
from ...sc_services.UsersService import get_user, add_user
from ...sc_common.authenticate import generate_token


def get_users_from_ad_handler(middleware):
    ad_users = get_ad_users(middleware.database)
    response_users = []
    for user in ad_users:
        response_users.append({
            "name": user.name,
            "full_name": user.full_name,
            "department": user.department,
            "mail": user.mail,
            "phone": user.phone,
            "registred": user.registred,
            "last_logon": user.last_logon,
            "isDeleted": user.isDeleted,
            "isLocked": user.isLocked,
            "updated": user.updated,
            "created": user.created,
        })
    middleware.set_data('users', response_users)
    return middleware.success().get()


def get_user_role_handler(middleware):
    '''Function for getting information about computers in districts according'''
    for service in middleware.district.services.get_active_directory_services():
        service.create_connection()
        x = service.get_users()
    return '{}'


def authenticate_handler(middleware):
    data = middleware.body
    if isinstance(data, dict)\
        and 'login' in data\
        and 'password' in data:
        if middleware.district.services.authenticate_user(data['login'], data['password']):
            user = get_user(middleware.database, data['login'])
            if not user:
                user = add_user(data['login'], get_ad_user(g.response.database, data['login']))
                g.response.database.session.commit()
            middleware.success()
            middleware.set_data('Bearer', generate_token(user.id))
            return middleware.get()
    return middleware.unauth().get()


def registration_handler(middleware):
    return '{}'
