from datetime import datetime
from flask import g, Blueprint

from ..handlers.CommonHandlers import get_now_handler, os_notificate_handler

mod = Blueprint('common', __name__, url_prefix='/common/')


@mod.route('/os_notificate/<computer_name>/', methods=['POST'])  # todo
def os_notificate(computer_name):
    middleware = g.middleware
    # print(request.get_data())
    # data = json.loads(request.get_data())
    # print(data)
    # database.Logons.login(computername, data['username'], data['os'], data['adapters'], _domain_server=data['domain_server'])
    # for patch in data['patches']:
    #     database.Patches.attach_patch(computername, patch)
    return os_notificate_handler


@mod.route('/now', methods=['GET'])
def get_now():
    middleware = g.middleware
    return get_now_handler(middleware)
