from flask import g

from backend.sc_actions.active_directory import update_computers_from_ad, update_users_from_ad, update_ad_users as upd_ad_users
from backend.sc_actions.computers import update_computers_unit
from backend.sc_actions.dallas_lock import update_computers_from_dallas
from backend.sc_actions.kaspersky import update_computers_from_kaspersky
from backend.sc_actions.puppet import update_computers_from_puppet
from backend.sc_actions.units import build_structure
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
    def update_kaspersky(district_name):
        '''

        EN:Function for updating information about computers from all active Kasperksy Service.
        RU:Функция обноления данных из всех активных сервисов Касперского.

        '''
        res = g.response
        district = res.district
        database = district.database
        build_structure(database, district.structure)
        update_computers_from_kaspersky(database, district)
        return res.success().get()
