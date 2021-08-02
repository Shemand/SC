from datetime import datetime

from ...sc_services.UnitsService import build_structure


def os_notificate_handler(middleware):
    # print(request.get_data())
    # data = json.loads(request.get_data())
    # print(data)
    # database.Logons.login(computername, data['username'], data['os'], data['adapters'], _domain_server=data['domain_server'])
    # for patch in data['patches']:
    #     database.Patches.attach_patch(computername, patch)
    return "{}"


def get_now_handler(middleware):
    return str(int(datetime.now().timestamp() * 1000))


def reset_structure_handler(middleware):
    district = middleware.district
    database = district.database
    structure = district.structure
    build_structure(database, structure)
    return middleware.success(data={}).get()
