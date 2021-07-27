from datetime import datetime

from ....sc_actions.units import build_structure
from .BlueprintAttacher import BlueprintAttacher



def attach_common_routes(mod):
    @mod.route('/os_notificate/<computer_name>/', methods=['POST'])  # todo
    def os_notificate(res):
        # print(request.get_data())
        # data = json.loads(request.get_data())
        # print(data)
        # database.Logons.login(computername, data['username'], data['os'], data['adapters'], _domain_server=data['domain_server'])
        # for patch in data['patches']:
        #     database.Patches.attach_patch(computername, patch)
        return "{}"

    @mod.route('/now', methods=['GET'])
    def get_now(res):
        return str(int(datetime.now().timestamp() * 1000))

    @mod.route('/reset/structure', methods=['GET'])
    def reset_structure(res):
        district = res.district
        database = district.database
        structure = district.structure
        build_structure(database, structure)
        return res.success(data={}).get()