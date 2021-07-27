from flask import g

from ....sc_actions.active_directory import update_computers_from_ad, update_users_from_ad, update_ad_users as upd_ad_users
from ....sc_actions.computers import update_computers_unit
from ....sc_actions.dallas_lock import update_computers_from_dallas
from ....sc_actions.kaspersky import update_computers_from_kaspersky
from ....sc_actions.puppet import update_computers_from_puppet
from ....sc_actions.units import build_structure
from .BlueprintAttacher import BlueprintAttacher


def attach_update_routes(mod): #todo edit the handlers
    @mod.route('/<district_name>/update/ad/computers', methods=['POST'])
    def update_ad_computers(district_name):
        '''

        EN:Function for updating information about computers in Active Directory.
        RU:Функция обноления данных из всех сервисов Active Directory.

        '''
        res = g.response
        district = res.district
        update_computers_from_ad(res.database, district)
        return res.success().get()

    @mod.route('/<district_name>/update/ad/users', methods=['POST'])
    def update_ad_users(district_name):
        '''

        EN:Function for updating information about users in Active Directory.
        RU:Функция обноления данных из всех сервисов Active Directory.

        '''
        res = g.response
        district = res.district
        upd_ad_users(res.database, district)
        return res.success().get()

    @mod.route('/<district_name>/update/puppet', methods=['POST'])
    def update_puppet_computers(district_name):
        '''

        EN:Function for updating information about computers from dallas lock.
        RU:Функция обноления данных из всех сервисов dallas lock.

        '''
        res = g.response
        district = res.district
        update_computers_from_puppet(res.database, district)
        return res.success().get()


    @mod.route('/<district_name>/update/dallas', methods=['POST'])
    def update_dallas_computers(district_name):
        '''

        EN:Function for updating information about computers from dallas lock.
        RU:Функция обноления данных из всех сервисов dallas lock.

        '''
        res = g.response
        district = res.district
        update_computers_from_dallas(res.database, district)
        return res.success().get()

    @mod.route('/<district_name>/update/reset/structure', methods=['POST'])
    def reset_ad_structure(district_name):
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

    @mod.route('/<district_name>/update/kaspersky', methods=['POST'])
    def update_kaspersky_computers(district_name):
        '''

        EN:Function for updating information about computers from all active Kaspersky Service.
        RU:Функция обноления данных из всех активных сервисов Касперского.

        '''
        res = g.response
        district = res.district
        database = district.database
        build_structure(database, district.structure)
        try:
            update_computers_from_kaspersky(database, district)
        except Exception as e:
            print(e)
            res.error().get()
        return res.success().get()

    @mod.route('/<district_name>/update/computers', methods=['POST'])
    def update_computers(district_name):
        try:
            update_ad_status = update_ad_computers(district_name)
        except Exception as e:
            update_ad_status = e
        try:
            update_kaspersky_status = update_kaspersky_computers(district_name)
        except Exception as e:
            update_kaspersky_status = e
        try:
            update_dallas_status = update_dallas_computers(district_name)
        except Exception as e:
            update_dallas_status = e
        try:
            update_puppet_status = update_puppet_computers(district_name)
        except Exception as e:
            update_puppet_status = e
        print(update_ad_status)
        print(update_kaspersky_status)
        print(update_dallas_status)
        print(update_puppet_status)
        return g.response.success().get()
