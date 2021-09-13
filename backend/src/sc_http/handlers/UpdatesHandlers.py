from flask import g



def update_ad_computers_handler(middleware):
    '''

    EN:Function for updating information about computers in Active Directory.
    RU:Функция обноления данных из всех сервисов Active Directory.

    '''
    district = middleware.district
    update_computers_from_ad(middleware.database, district)
    return middleware.success().get()

def update_ad_users_handler(middleware):
    '''

    EN:Function for updating information about users in Active Directory.
    RU:Функция обноления данных из всех сервисов Active Directory.

    '''
    district = middleware.district
    upd_ad_users(middleware.database, district)
    return middleware.success().get()

def update_puppet_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from dallas lock.
    RU:Функция обноления данных из всех сервисов dallas lock.

    '''
    district = middleware.district
    update_computers_from_puppet(middleware.database, district)
    return middleware.success().get()


def update_dallas_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from dallas lock.
    RU:Функция обноления данных из всех сервисов dallas lock.

    '''
    district = middleware.district
    update_computers_from_dallas(middleware.database, district)
    return middleware.success().get()

def reset_ad_structure_handler(middleware):
    '''

    EN:Function for reset structure specified in configuration file of district
    RU:Функция сброка структуры подразделений в соответсвии с описанной в конфигурационном файле округа (district).

    '''
    district = middleware.district
    database = district.database
    build_structure(database, district.structure)
    update_computers_unit(database)
    return middleware.success().get()

def update_kaspersky_computers_handler(middleware):
    '''

    EN:Function for updating information about computers from all active Kaspersky Service.
    RU:Функция обноления данных из всех активных сервисов Касперского.

    '''
    district = middleware.district
    database = district.database
    build_structure(database, district.structure)
    update_computers_from_kaspersky(database, district)
        # res.error().get()
    return middleware.success().get()

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
