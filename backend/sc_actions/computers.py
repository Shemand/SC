from backend.sc_actions.functions import rows_to_dicts
from backend.sc_database.model.Computers import Computers
from backend.sc_database.model.Users import Users


def get_computers(database):
    computers = database.session.query(Computers).all()
    return rows_to_dicts(computers)


def get_computer(database, computer_name):
    computer = database.session.query(Computers).filter_by(name=computer_name).first()
    if not computer:
        return None
    return rows_to_dicts(computer)


def create_computer(database, computer_name):
    computer = Computers(name=computer_name)
    database.session.add(computer)
    database.commit()
    return get_computer(database, computer_name)


def get_or_create_computer(database, computer_name):
    computer = get_computer(database, computer_name)
    if computer:
        return computer
    return create_computer(database, computer_name)
