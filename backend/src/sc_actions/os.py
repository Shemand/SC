from ..sc_database.model.Addresses import Addresses
from ..sc_database.model.OperationSystems import OperationSystems


def get_os_all(database):
    return database.session.query(Addresses).all()


def get_os_by_name(database, os_name):
    os = database.session.query(OperationSystems).filter_by(name=os_name).first()
    if not os:
        return None
    return os


def get_os_by_id(database, os_id):
    os = database.session.query(OperationSystems).filter_by(id=os_id).first()
    if not os:
        return None
    return os


def create_os(database, os_name):
    params = {
        "name": os_name,
        "isUnix": False if os_name is None\
            else
            False if 'WIN' in os_name.upper() else True
    }
    os = OperationSystems(**params)
    database.session.add(os)
    database.commit()
    return os


def get_or_create_os(database, os_name):
    os = get_os_by_name(database, os_name)
    if os:
        return os
    return create_os(database, os_name)


def is_exists_os(database, os_name):
    os = get_os_by_name(database, os_name)
    if os:
        return True
    return False
