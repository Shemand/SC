from datetime import datetime

from .computers import get_computers, create_computer, inject_row_in_computers_records
from .functions import delete_from_list_by_hash
from .users import inject_row_in_users_records, get_users
from ..sc_common.functions import reformat_computer_name
from ..sc_database.model.Computers_ActiveDirectory import Computers_ActiveDirectory
from ..sc_database.model.Users_ActiveDirectory import Users_ActiveDirectory


# ----- public function

def get_ad_user(database, user_name):
    return database.session.query(Users_ActiveDirectory).filter_by(name=user_name).first()


def get_ad_users(database):
    return database.session.query(Users_ActiveDirectory).all()


def delete_computer_from_ad(database, computer_id):
    ad_computers = database.session.query(Computers_ActiveDirectory).filter_by(Computers_id=computer_id).all()
    for computer in ad_computers:
        computer.isDeleted = datetime.now()
    database.session.commit()


def create_computer_ad_record(database, computer_row, ad_record):
    params = {
        "Computers_id": computer_row.id,
        "last_visible": ad_record['last_logon'],
        "registred": ad_record['whenCreated']
    }
    row = Computers_ActiveDirectory(**params)
    database.session.add(row)
    # database.session.commit()
    return row


def create_user_ad_record(database, ad_record):
    params = {
        "name": ad_record['account_name'],
        "full_name": ad_record['name'],
        "department": ad_record['department'],
        "mail": ad_record['mail'],
        "phone": ad_record['phone'],
        "registred": ad_record['whenCreated'],
        "last_logon": ad_record['last_logon'],
        "isDisabled": datetime.now() if ad_record['disabled'] else None,
        "isLocked": datetime.now() if ad_record['locked'] else None
    }
    row = Users_ActiveDirectory(**params)
    database.session.add(row)
    database.session.commit()
    return row


# ----- update computers data -----

def update_computers_from_ad(database, district):
    ad_services = district.services.get_active_directory_services()
    ad_rows = _get_ad_computers_rows(database)
    records_ad = []
    for service in ad_services:
        records_ad.extend(_get_ad_computer_records(database, service))
    inject_row_in_computers_records(database, records_ad)
    for record in records_ad:
        required_ad_row = None
        for row in ad_rows:
            if row.Computers_id == record['computer'].id \
                    and row.registred == record['whenCreated']:
                required_ad_row = row
                break
        if not required_ad_row:
            create_computer_ad_record(database, record['computer'], record)
        else:
            _update_computer_ad_record(database, required_ad_row, record)
            delete_from_list_by_hash(ad_rows, required_ad_row)
    for row in ad_rows:
        row.isDeleted = datetime.now()
    database.session.commit()
    return True


def _get_ad_computer_records(database, ad_service):
    if ad_service.check_connection():
        return ad_service.get_computers()


def _get_ad_computers_rows(database):
    return database.session.query(Computers_ActiveDirectory).all()


def _update_computer_ad_record(database, ad_row, ad_record):
    if ad_row.last_visible != ad_record['last_logon']:
        ad_row.last_visible = ad_record['last_logon']
    if not ad_row.isActive != ad_record['disabled']:
        ad_row.isActive = not ad_record['disabled']
    # database.session.commit()
    return ad_row


def _computer_ad_record_in_list(database, ad_records, computer_row):
    for ad_record in ad_records:
        if computer_row.name == ad_record.name:
            if computer_row['last_visible'] == ad_record['last_logon']:
                return ad_record
    return None


# ----- update ad users -----

def update_ad_users(database, district):
    ad_services = district.services.get_active_directory_services()
    ad_rows = {row.name: row for row in get_ad_users(database)}
    users_rows = {row.login: row for row in get_users(database)}
    records_ad = []
    for service in ad_services:
        records_ad.extend(_get_ad_users_records(database, service))
    for record in records_ad:
        user_name = record['account_name']
        if user_name in ad_rows:
            record['ad_row'] = ad_rows[user_name]
            del ad_rows[user_name]
        else:
            record['ad_row'] = create_user_ad_record(database, record)
        record['user_row'] = users_rows.get(user_name, None)
    for record in records_ad:
        ad_row = record['ad_row']
        _update_user_ad_row(record)
    for user_name, row in ad_rows.items():
        row.isDeleted = datetime.now()
    database.session.commit()
    return True


def update_users_from_ad(database, district):
    ad_services = district.services.get_active_directory_services()
    ad_rows = get_ad_users(database)
    records_ad = []
    for service in ad_services:
        records_ad.extend(_get_ad_users_records(database, service))
    inject_row_in_users_records(database, records_ad)
    for record in records_ad:
        required_ad_row = None
        for row in ad_rows:
            if row.login == record['computer'].id \
                    and row.registred == record['whenCreated']:
                required_ad_row = row
                break
        if not required_ad_row:
            create_computer_ad_record(database, record['computer'], record)
        else:
            _update_computer_ad_record(database, required_ad_row, record)
            delete_from_list_by_hash(ad_rows, required_ad_row)
    for row in ad_rows:
        row.isDeleted = datetime.now()
    database.session.commit()
    return True


def _get_ad_users_records(database, ad_service):
    if ad_service.check_connection():
        return ad_service.get_users()


def _update_user_ad_row(record):
    row = record['ad_row']
    if record['user_row'] is not None \
            and record['user_row'].Users_ActiveDirectory_id != row.id:
        record['user_row'].Users_ActiveDirectory_id = row.id
    if row.isDeleted is not None:
        row.isDeleted = None
    if record['name'] != row.full_name:
        row.full_name = record['name']
    if record['account_name'] != row.name:
        row.name = record['account_name']
    if record['last_logon'] != row.last_logon:
        row.last_logon = record['last_logon']
    if record['mail'] != row.mail:
        row.mail = record['mail']
    if record['phone'] != row.phone:
        row.phone = record['phone']
    if record['department'] != row.department:
        row.department = record['department']
    if record['locked'] and row.isLocked is None:
        row.isLocked = datetime.now()
    elif row.isLocked and not record['locked']:
        row.isLocked = None
    if record['disabled'] and row.isDisabled is None:
        row.isDisabled = datetime.now()
    elif row.isDisabled and not record['disabled']:
        row.isDisabled = None
