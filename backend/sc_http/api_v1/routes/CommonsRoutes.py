from datetime import datetime

from backend.sc_actions.units import build_structure
from .BlueprintAttacher import BlueprintAttacher


class CommonsRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/os_notificate/<computer_name>/', methods=['POST'])  # todo
        def os_notificate(res):
            # print(request.get_data())
            # data = json.loads(request.get_data())
            # print(data)
            # database.Logons.login(computername, data['username'], data['os'], data['adapters'], _domain_server=data['domain_server'])
            # for patch in data['patches']:
            #     database.Patches.attach_patch(computername, patch)
            return "{}"

        @route('/now', methods=['GET'])
        def get_now(res):
            return str(int(datetime.now().timestamp() * 1000))

        @route('/reset/structure', methods=['GET'])
        def reset_structure(res):
            district = res.district
            database = district.database
            structure = district.structure
            build_structure(database, structure)
            return res.success(data={}).get()