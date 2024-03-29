from datetime import datetime
from typing import List


def reformat_computer_name(name):
    name = name.upper()
    name = name.split('/')[0]
    edited = True
    while edited:
        edited = False
        if name.rfind('~~') != -1:
            name = name[0:name.find('~~')]
            edited = True
        if name.rfind('.ROSGVARD.RU') != -1:
            name = name[0:name.rfind('.ROSGVARD.RU')]
            edited = True
        if name.rfind('.') != -1:
            name = name[0:name.rfind('.')]
            edited = True
        if name.rfind('(') != -1:
            name = name[0:name.rfind('(')]
            edited = True
        if name.rfind('[') != -1:
            name = name[0:name.rfind('[')]
            edited = True
        if name.rfind(' ') != -1:
            name = name[0:name.rfind(' ')]
            edited = True
    return name


def reformat_unit_name(name):
    return name.upper()


def transformate_time(value):
    if isinstance(value, List) and len(value) > 0:
        value =  datetime.utcfromtimestamp(int(value[0])).replace(tzinfo=None)
        if value < datetime.now():
            return value
    elif isinstance(value, datetime):
        value = value.replace(tzinfo=None)
        if value < datetime.now():
            return value
    elif isinstance(value, int):
        value = datetime.utcfromtimestamp(value).replace(tzinfo=None)
        if value < datetime.now():
            return value
    return None


def extract_unit_from_name(computer_name):
    end = computer_name.find('-')
    if end != -1:
        return reformat_unit_name(computer_name[:end])
    return 'UNKNOWN'


def rows_to_dicts(rows):
    if isinstance(rows, list):
        for row in rows:
            if '_sa_instance_state' in row.__dict__:
                del row.__dict__['_sa_instance_state']
        return [dict(row.__dict__) for row in rows]
    else:
        if '_sa_instance_state' in rows.__dict__:
            del rows.__dict__['_sa_instance_state']
        return dict(rows.__dict__)


def delete_from_list_by_hash(array, element):
    hash = id(element)
    index = 0
    for element in array:
        if id(element) == hash:
            array.pop(index)
            break
        index += 1
