from .UnitsService import get_or_create_unit, get_unit_by_id, get_unit_by_name
from ..sc_common.functions import reformat_computer_name, extract_unit_from_name, reformat_unit_name
from ..sc_repositories.DatabaseModels.Computers import Computers
from ..sc_repositories.DatabaseModels.Units import Units


def get_computers(database):
    computers = database.session.query(Computers).all()
    return computers


def get_computer(database, computer_name):
    computer = database.session.query(Computers).filter_by(name=computer_name).first()
    if not computer:
        return None
    return computer


def create_computer(database, computer_name):
    unit_name = extract_unit_from_name(computer_name)
    unit = database.session.query(Units).filter_by(name=unit_name).first()
    if not unit:
        unit = get_or_create_unit(database, 'UNKNOWN')
    computer = Computers(name=reformat_computer_name(computer_name), Units_id=unit.id)
    database.session.add(computer)
    database.commit()
    return computer

def get_or_create_computer(database, computer_name):
    computer = get_computer(database, computer_name)
    if computer:
        return computer
    return create_computer(database, computer_name)

def is_exists_computer(database, computer_name):
    computer = get_computer(database, computer_name)
    if computer:
        return True
    return False

def inject_row_in_computers_records(database, records, name_field='name'):
    computers = { reformat_computer_name(computer.name) : computer for computer in get_computers(database) }
    if isinstance(records, list):
        for record in records:
            computer_name = record[name_field]
            if not computer_name in computers:
                computers[computer_name] = create_computer(database, computer_name)
            record['computer'] = computers[computer_name]
    elif isinstance(records, dict):
        to_remove = []
        for computer_name, d in records.items():
            computer_name = reformat_computer_name(computer_name)
            print(computer_name)
            if records[computer_name] == None:
                to_remove.append(computer_name)
                continue
            if not computer_name in computers:
                computers[computer_name] = create_computer(database, computer_name)
                records[computer_name] = computers[computer_name]
            else:
                d['computer'] = computers[computer_name]
        for computer_name in to_remove:
            del records[computer_name]
    else:
        raise RuntimeError('computers.inject_row_in_computers_records isn\'t dict or list')


def change_computer_unit_by_name(database, computer_name, unit_name):
    computer = get_computer(database, computer_name)
    change_computer_unit(database, computer, unit_name)

def change_computer_unit(database, computer_obj, unit_name):
    if computer_obj:
        unit = get_unit_by_name(database, reformat_unit_name(unit_name))
        if unit:
            if computer_obj.Units_id != unit.id:
                computer_obj.Units_id = unit.id
                database.session.commit()
            return computer_obj
        print(f'change_computer_unit: Unknown unit with this name ({unit_name})')
        return None
    print(f'change_computer_unit: Unknown computer with this name ({computer_obj.name})')
    return None

def update_computers_unit(database):
    computers = get_computers(database)
    for computer in computers:
        unit_name = extract_unit_from_name(computer.name)
        change_computer_unit(database, computer, unit_name)
