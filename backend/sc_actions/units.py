from backend.sc_database.model.Units import Units

def get_default_unit(database):
    return get_unit_by_name(database, 'UNKNOWN')

def get_units_all(database):
    return database.session.query(Units).all()


def get_unit_by_name(database, name):
    unit = database.session.query(Units).filter_by(name=name).first()
    if not unit:
        return None
    return unit


def get_unit_by_id(database, unit_id):
    unit = database.session.query(Units).filter_by(id=unit_id).first()
    if not unit:
        return None
    return unit


def create_unit(database, unit_name, parent_unit_name=None):
    unit = get_unit_by_name(database, unit_name)
    if unit:
        raise RuntimeError(f'create_unit: unit with name ({unit_name}) already exists')
    parent_unit = None
    if parent_unit_name:
        parent_unit = get_unit_by_name(database, parent_unit_name)
        if not parent_unit:
            raise RuntimeError(f'create_unit: parent_unit_name ({parent_unit_name}) didn\'t found')
    params = {
        "name": unit_name,
        "root_id": parent_unit.id if parent_unit else None
    }
    unit = Units(**params)
    database.session.add(unit)
    database.commit()
    return unit


def get_or_create_unit(database, unit_name, root_name=None):
    unit = get_unit_by_name(database, unit_name)
    if unit:
        return unit
    return create_unit(database, unit_name, root_name)


def change_relation(database, unit_name, parent_unit_name):
    unit = get_unit_by_name(database, unit_name)
    parent_unit_name = get_unit_by_name(database, parent_unit_name)
    if unit and parent_unit_name:
        unit.root_id = parent_unit_name.id
        database.session.commit()
        return
    else:
        raise RuntimeError(f'change_relation: unit_name ({unit_name}) or parent_unit_name ({parent_unit_name}) didn\'t found id database.')


def build_structure(database, dict_structure):
    for unit_name, children in dict_structure.items():
        unit = get_or_create_unit(database, unit_name)
        __build_units(database, unit_name, children)
    database.session.commit()


def __build_units(database, unit_name, children):
    unit = get_unit_by_name(database, unit_name)
    for child_name, children in children.items():
        child = get_unit_by_name(database, child_name)
        if child:
            child.root_id = unit.id
        else:
            child = create_unit(database, child_name, unit.name)
        if children != {}:
            __build_units(database, child_name, children)


def get_units_list(database):
    return [unit.name for unit in database.query(Units).all()]


def get_available_units_id(database, root_unit_name):
    next_ids= []
    next_ids.append(get_unit_by_name(database, root_unit_name).id)
    for id in next_ids:
        next_ids.extend([ unit.id for unit in database.session.query(Units).filter_by(root_id=id).all() ])
    return next_ids
