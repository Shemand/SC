from flask import Blueprint, g

from ..handlers.DevicesHandlers import change_device_type_handler, remove_device_handler, \
    add_device_handler, get_devices_handler

mod = Blueprint('Devices', __name__, url_prefix='/devices/')


@mod.route('/devices', methods=['GET'])
def get_devices():
    middleware = g.middleware
    return get_devices_handler(middleware)

@mod.route('/add', methods=['PUT'])
def add_device():
    middleware = g.middleware
    return add_device_handler(middleware)

@mod.route('/remove/<device_id>', methods=['DELETE'])
def remove_device(device_id):
    middleware = g.middleware
    return remove_device_handler(middleware, device_id)

@mod.route('/<device_id>/comment', methods=['PUT'])
def set_device_comment(device_id):
    middleware = g.middleware
    return set_device_comment(middleware, device_id)

@mod.route('/<device_name>/type/<type>', methods=['PUT'])
def change_device_type(device_name, type):
    middleware = g.middleware
    return change_device_type_handler(middleware, device_name, type)
