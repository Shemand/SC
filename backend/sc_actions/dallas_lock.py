from datetime import datetime


# ----- public function
from backend.sc_actions.computers import get_or_create_computer
from backend.sc_database.model.DallasLock import DallasLock

def get_dallas_computers(database):
    return database.session.query(DallasLock).all()

def create_computer_dallas_record(database, computer_row, dallas_record):
    params = {
        "Computers_id": computer_row.id,
        "status": dallas_record['status'],
        "server": dallas_record['server']
    }
    row = DallasLock(**params)
    database.session.add(row)
    # database.session.commit()
    return row

# ----- update computers data -----

def update_computers_from_dallas(database, district):
    records_dallas = {record['name'] : record for record in _get_dallas_computer_records(database, district)}
    rows_dallas = rows_dallas = { row.Computers_id : row for row in get_dallas_computers(database) }
    _inject_row_in_computer_records(database, records_dallas, rows_dallas)
    for _, record in records_dallas.items():
        if record['dallas_row'] == None:
            record['dallas_row'] = create_computer_dallas_record(database, record['computer_row'], record)
        else:
            _update_computer_dallas_row(database, record['dallas_row'], record)
    for computer_id, row in rows_dallas.items():
        row.isDeleted = datetime.now()
        row.updated = datetime.now()
    database.session.commit()
    return True


def _get_dallas_computer_records(database, district):
    records = []
    for service in district.services.get_dallas_lock_services():
        records.extend(service.get_computers())
    return records


def _inject_row_in_computer_records(database, records, rows_dallas):
    for computer_name, record in records.items():
        computer_row = get_or_create_computer(database, computer_name)
        record['computer_row'] = computer_row
        if computer_row.id in rows_dallas:
            record['dallas_row'] = rows_dallas[computer_row.id]
            del rows_dallas[computer_row.id]
        else:
            record['dallas_row'] = None


def _update_computer_dallas_row(database, dallas_row, dallas_record):
    if dallas_row.status != dallas_record['status']:
        dallas_row.status = dallas_record['status']
    if dallas_row.server != dallas_record['server']:
        dallas_row.server = dallas_record['server']
    if dallas_row.isDeleted is not None:
        dallas_row.isDeleted = None
    return dallas_row
