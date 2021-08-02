import json

from flask import g, request

from ...sc_services.ComputersFrameService import get_computers_frame, FROM_ACTIVE_DIRECTORY, FROM_PUPPET, FROM_KASPERSKY, FROM_DALLAS_LOCK


def get_computers_info_handler(middleware):
    """Function for getting all information about computer"""
    res = g.response
    units = res.user.available_units
    args = request.args
    puppet = args['puppet'] if 'puppet' in args else None
    active_directory = args['active_directory'] if 'active_directory' in args else None
    dallas_lock = args['dallas_lock'] if 'dallas_lock' in args else None
    kaspersky = args['kaspersky'] if 'kaspersky' in args else None
    sources = {}
    if puppet:
        sources[FROM_PUPPET] = json.loads(puppet)
    if active_directory:
        sources[FROM_ACTIVE_DIRECTORY] = json.loads(active_directory)
    if kaspersky:
        sources[FROM_KASPERSKY] = json.loads(kaspersky)
    if dallas_lock:
        sources[FROM_DALLAS_LOCK] = json.loads(dallas_lock)
    data = get_computers_frame(res.database,
                               units,
                               sources=sources)
    res.set_data('computers', data)
    return res.success().get()

def set_computer_comment_handler(middleware, computer_id):
    """Function for changing comment of computer"""
    return '{}'

def change_computer_type_handler(middleware, computer_name, type):
    """Function for changing type of computer(ARM, Server)"""
    return '{}'

def lock_computer_handler(middleware, computer_name):
    """Function for locking computer by computer_name"""
    return '{}'

def unlock_computer_handler(middleware, computer_name):
    """Function for unlocking computer by computer_name"""
    return '{}'
