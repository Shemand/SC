from flask import g, Blueprint

from ..handlers.UpdatesHandlers import update_ad_users_handler, update_ad_computers_handler, \
    update_puppet_computers_handler, update_dallas_computers_handler, reset_ad_structure_handler, \
    update_kaspersky_computers_handler, update_computers_handler

mod = Blueprint('Updates', __name__, url_prefix='/update')


@mod.route('/ad/computers', methods=['POST'])
def update_ad_computers():
    middleware = g.middleware
    return update_ad_computers_handler(middleware)


@mod.route('/ad/users', methods=['POST'])
def update_ad_users():
    middleware = g.middleware
    return update_ad_users_handler(middleware)


@mod.route('/puppet', methods=['POST'])
def update_puppet_computers():
    middleware = g.middleware
    return update_puppet_computers_handler(middleware)


@mod.route('/dallas', methods=['POST'])
def update_dallas_computers():
    middleware = g.middleware
    return update_dallas_computers_handler(middleware)


@mod.route('/reset/structure', methods=['POST'])
def reset_ad_structure():
    middleware = g.middleware
    return reset_ad_structure_handler(middleware)


@mod.route('/kaspersky', methods=['POST'])
def update_kaspersky_computers():
    middleware = g.middleware
    return update_kaspersky_computers_handler(middleware)


@mod.route('/computers', methods=['POST'])
def update_computers():
    middleware = g.middleware
    return update_computers_handler(middleware)
