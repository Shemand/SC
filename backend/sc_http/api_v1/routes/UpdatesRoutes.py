from backend.sc_actions.active_directory import update_computers_from_ad
from backend.sc_actions.computers import update_computers_unit
from backend.sc_actions.units import build_structure
from .BlueprintAttacher import BlueprintAttacher


class UpdatesRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/ad', methods=['GET'])
        def update_active_directory(res):
            '''

            EN:Function for updating information about computers in Active Directory.
            RU:Функция обноления данных из всех сервисов Active Directory.

            '''
            district = res.district
            database = district.database
            update_computers_from_ad(database, district)
            return res.success({}).get()

        @route('/reset/structure', methods=['GET'])
        def reset_ad_structure(res):
            '''

            EN:Function for reset structure specified in configuration file of district
            RU:Функция сброка структуры подразделений в соответсвии с описанной в конфигурационном файле округа (district).

            '''
            district = res.district
            database = district.database
            build_structure(database, district.structure)
            update_computers_unit(database)
            return res.success({}).get()

        @route('/kaspersky', methods=['GET'])
        def update_kaspersky(res):
            '''

            EN:Function for updating information about computers from all active Kasperksy Service.
            RU:Функция обноления данных из всех активных сервисов Касперского.

            '''
            district = res.district
            database = district.database
            build_structure(database, district.structure)
            update_computers_unit(database)
            return res.success({}).get()
