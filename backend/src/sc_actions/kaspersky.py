from datetime import datetime

from .computers import inject_row_in_computers_records
from .functions import delete_from_list_by_hash
from .ip import get_or_create_ip, get_ip_by_address
from .os import get_or_create_os, get_os_by_name
from ..sc_database.model.Kaspersky import Kaspersky


def update_computers_from_kaspersky(database, district):
    kaspersky_services = district.services.get_kaspersky_services()
    kaspersky_rows = _get_kaspersky_records_from_database(database)
    records_kaspersky = {}
    updated_servers = []
    for service in kaspersky_services:
        try:
            records_kaspersky = {**records_kaspersky, **_get_kaspersky_records_from_service(database, service)}
            updated_servers.append(service.server)
        except Exception:
            continue
    inject_row_in_computers_records(database, records_kaspersky)
    for _, record in records_kaspersky.items():
        required_kaspersky_row = None
        for row in kaspersky_rows:
             if row.Computers_id == record['computer'].id:
                required_kaspersky_row = row
                break
        if not required_kaspersky_row:
            _create_kaspersky_record(database, record['computer'], record)
        else:
            _update_kaspersky_record(database, required_kaspersky_row, record)
            delete_from_list_by_hash(kaspersky_rows, required_kaspersky_row)
    for row in kaspersky_rows:
        if row.server in updated_servers:
            row.isDeleted = datetime.now()
    database.session.commit()
    return True


def _get_kaspersky_records_from_service(database, kaspersky_service):
    if kaspersky_service.check_connection():
        return kaspersky_service.get_computers()


def _get_kaspersky_records_from_database(database):
    return database.session.query(Kaspersky).all()


def _create_kaspersky_record(database, computer_row, kaspersky_record):
    params = {
        "Computers_id" : computer_row.id,
        "OperationSystems_id" : get_or_create_os(database, kaspersky_record['os']).id,
        "Addresses_id" : get_or_create_ip(database, kaspersky_record['ip']).id,
        "agent_version" : kaspersky_record['agent_version'],
        "security_version" : kaspersky_record['security_version'],
        "server" : kaspersky_record['server']
    }
    row = Kaspersky(**params)
    database.session.add(row)
    database.session.commit()
    return row


def _update_kaspersky_record(database, kaspersky_row, kaspersky_record):
    if kaspersky_row.isDeleted != None:
        kaspersky_row.isDeleted = None
    if kaspersky_row.OperationSystems_id != get_os_by_name(database, kaspersky_record['os']):
        kaspersky_row.OperationSystems_id = get_or_create_os(database, kaspersky_record['os']).id
    if kaspersky_row.Addresses_id != get_ip_by_address(database, kaspersky_record['ip']):
        kaspersky_row.Addresses_id = get_or_create_ip(database, kaspersky_record['ip']).id
    if kaspersky_row.agent_version != kaspersky_record['agent_version']:
        kaspersky_row.agent_version = kaspersky_record['agent_version']
    if kaspersky_row.security_version != kaspersky_record['security_version']:
        kaspersky_row.security_version = kaspersky_record['security_version']
    if kaspersky_row.server != kaspersky_record['server']:
        kaspersky_row.server = kaspersky_record['server']
    database.session.commit()
    return kaspersky_row


def _delete_from_kaspersky(database, computer_id):
    kaspersky = database.session.query(Kaspersky).filter_by(Computers_id=computer_id).all()
    for computer in kaspersky:
        computer.isDeleted = datetime.now()
    database.session.commit()