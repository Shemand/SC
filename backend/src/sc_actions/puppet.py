from datetime import datetime


# ----- public function
from .computers import get_or_create_computer
from .ip import get_ip_all, get_or_create_ip
from .os import get_or_create_os
from ..sc_database.model.Puppets import Puppets


def get_puppet_computers(database):
    return database.session.query(Puppets).all()


def create_computer_puppet_record(database, record):
    params = {
        "Computers_id": record['computer_row'].id,
        "Addresses_id": record['ip_row'].id if record['ip_row'] else None,
        "OperationSystems_id": record['os_row'].id if record['os_row'] else None,
        "board_serial_number": record['boardserialnumber'],
        "astra_update": record['astra_update_version'],
        "environment": record['environment'],
        "domain": record['domain'],
        "serial_number": record['serial_number'],
        "isVirtual": record['is_virtual'],
        "mac": record['macaddress'],
        "kesl_version": record['kesl_astra_version'],
        "klnagent_version": record['klnagent_astra_version'],
        "uptime_seconds": record['uptime_seconds']
    }
    row = Puppets(**params)
    database.session.add(row)
    # database.session.commit()
    return row

# ----- update computers data -----


def update_computers_from_puppet(database, district):
    records_puppet = _get_puppet_records(database, district)
    rows_puppet = { row.Computers_id : row for row in get_puppet_computers(database) }
    _inject_rows_in_records(database, records_puppet)
    for _, record in records_puppet.items():
        puppet_row = rows_puppet.get(record['computer_row'].id, None)
        if puppet_row is not None:
            del rows_puppet[record['computer_row'].id]
            _update_puppet_row(database, puppet_row, record)
        else:
            create_computer_puppet_record(database, record)
    for computer_id, row in rows_puppet.items():
        row.isDeleted = datetime.now()
        row.updated = datetime.now()
    database.session.commit()
    return True


def _get_puppet_records(database, district):
    records = {}
    for service in district.services.get_puppet_services():
        records = {**records, **service.get_computers()}
    return records


def _update_puppet_row(database, puppet_row, puppet_record):
    ip_row_id = puppet_record['ip_row'].id if puppet_record['ip_row'] else None
    os_row_id = puppet_record['os_row'].id if puppet_record['os_row'] else None
    if puppet_row.Computers_id != puppet_record['computer_row'].id:
        puppet_row.Computers_id = puppet_record['computer_row'].id
    if puppet_row.Addresses_id != ip_row_id:
        puppet_row.Addresses_id = ip_row_id
    if puppet_row.OperationSystems_id != os_row_id:
        puppet_row.OperationSystems_id = os_row_id
    if puppet_row.board_serial_number != puppet_record['boardserialnumber']:
        puppet_row.board_serial_number = puppet_record['boardserialnumber']
    if puppet_row.astra_update != puppet_record['astra_update_version']:
        puppet_row.astra_update = puppet_record['astra_update_version']
    if puppet_row.environment != puppet_record['environment']:
        puppet_row.environment = puppet_record['environment']
    if puppet_row.domain != puppet_record['domain']:
        puppet_row.domain = puppet_record['domain']
    if puppet_row.serial_number != puppet_record['serial_number']:
        puppet_row.serial_number = puppet_record['serial_number']
    if puppet_row.isVirtual != puppet_record['is_virtual']:
        puppet_row.isVirtual = puppet_record['is_virtual']
    if puppet_row.mac != puppet_record['macaddress']:
        puppet_row.mac = puppet_record['macaddress']
    if puppet_row.kesl_version != puppet_record['kesl_astra_version']:
        puppet_row.kesl_version = puppet_record['kesl_astra_version']
    if puppet_row.klnagent_version != puppet_record['klnagent_astra_version']:
        puppet_row.klnagent_version = puppet_record['klnagent_astra_version']
    if puppet_row.uptime_seconds != puppet_record['uptime_seconds']:
        puppet_row.uptime_seconds = puppet_record['uptime_seconds']
    if puppet_row.isDeleted != None:
        puppet_row.isDeleted = None

    return puppet_row

def _inject_rows_in_records(database, records_puppet):
    for computer_name, record in records_puppet.items():
        __inject_computer_in_records(database, record, computer_name)
        __inject_ip_in_records(database, record)
        __inject_os_in_records(database, record)

def __inject_computer_in_records(database, record, computer_name):
    record['computer_row'] = get_or_create_computer(database, computer_name)

def __inject_os_in_records(database, record):
    if 'os' in record and record['os']:
        os_name = record['os']['name'] + ' ' + record['os']['distro']['description']
        record['os_row'] = get_or_create_os(database, os_name)
    else:
        record['os_row'] = None

def __inject_ip_in_records(database, record):
    if 'ipaddress' in record and record['ipaddress']:
        record['ip_row'] = get_or_create_ip(database, record['ipaddress'])
    else:
        record['ip_row'] = None
