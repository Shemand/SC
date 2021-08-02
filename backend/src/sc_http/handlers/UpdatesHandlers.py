from flask import g

from ...sc_services.ActiveDirectoryService import update_computers_from_ad, update_users_from_ad as upd_ad_users
from ...sc_services.ComputersService import update_computers_unit
from ...sc_services.DallasLockService import update_computers_from_dallas
from ...sc_services.KasperskyService import update_computers_from_kaspersky
from ...sc_services.PuppetService import update_computers_from_puppet
from ...sc_services.UnitsService import build_structure


def update_ad_computers_handler(middleware):
    '''

    EN:Function for updating information about computers in Active Directory.
    RU:Функция обноления данных из всех сервисов Active Directory.

    '''
    res = g.response
    district = res.district
    update_computers_from_ad(res.database, district)
    return res.success().get()

def update_ad_users_handler(middleware):
    '''

    EN:Function for updating information about users in Active Directory.
    RU:Функция обноления данных из всех сервисов Active Directory.

    '''
    res = g.response
    district = res.district
    upd_ad_users(res.database, district)
    return res.success().get()

def update_puppet_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from dallas lock.
    RU:Функция обноления данных из всех сервисов dallas lock.

    '''
    res = g.response
    district = res.district
    update_computers_from_puppet(res.database, district)
    return res.success().get()


def update_dallas_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from dallas lock.
    RU:Функция обноления данных из всех сервисов dallas lock.

    '''
    res = g.response
    district = res.district
    update_computers_from_dallas(res.database, district)
    return res.success().get()

def reset_ad_structure_handler(middleware):
    '''

    EN:Function for reset structure specified in configuration file of district
    RU:Функция сброка структуры подразделений в соответсвии с описанной в конфигурационном файле округа (district).

    '''
    res = g.response
    district = res.district
    database = district.database
    build_structure(database, district.structure)
    update_computers_unit(database)
    return res.success().get()

def update_kaspersky_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from all active Kaspersky Service.
    RU:Функция обноления данных из всех активных сервисов Касперского.

    '''
    res = g.response
    district = res.district
    database = district.database
    build_structure(database, district.structure)
    update_computers_from_kaspersky(database, district)
        # res.error().get()
    return res.success().get()

def update_computers_handler(middleware):
    try:
        update_ad_status = update_computers_from_ad(middleware)
    except Exception as e:
        update_ad_status = e
    try:
        update_kaspersky_status = update_computers_from_kaspersky(middleware)
    except Exception as e:
        update_kaspersky_status = e
    try:
        update_dallas_status = update_computers_from_dallas(middleware)
    except Exception as e:
        update_dallas_status = e
    try:
        update_puppet_status = update_computers_from_puppet(middleware)
    except Exception as e:
        update_puppet_status = e
    print(update_ad_status)
    print(update_kaspersky_status)
    print(update_dallas_status)
    print(update_puppet_status)
    return g.response.success().get()
