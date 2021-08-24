import json

from flask import g, request, Blueprint

from ..handlers.UsersHandlers import get_users_from_ad_handler, get_user_role_handler, authenticate_handler, \
    registration_handler

mod = Blueprint('Users', __name__, url_prefix='/users')


@mod.route('/ad', methods=['GET'])
def get_users_from_ad():
    middleware = g.middleware
    return get_users_from_ad_handler(middleware)


@mod.route('/role', methods=['GET'])
def get_user_role():
    middleware = g.middleware
    return get_user_role_handler(middleware)


@mod.route('/auth', methods=['POST'])
def authenticate():
    middleware = g.middleware
    return authenticate_handler(middleware)


@mod.route('/registration', methods=['POST'])
def registration():
    middleware = g.middleware
    return registration_handler(middleware)
