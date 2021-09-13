from backend.sc_entities.Entities import Entities

def disabled_test_ad_services():
    district = Entities().get_district('SZO')
    services = district.services.get_active_directory_services()
    records = {}
    for service in services:
        service.create_connection()
        computers = service.all()
        for computer in computers:
            if computer['name'] in records:
                print(computer['name'] + ' is duplicate')
            records[computer['name']] = {}
    print('ff')

def test_dallas_services():
    district = Entities().get_district('SZO')
    services = district.services.get_dallas_lock_services()
    records = []
    for service in services:
        records.extend(service.all())

def test_puppet_services():
    district = Entities().get_district('SZO')
    services = district.services.get_puppet_services()
    records = []
    for service in services:
        records.extend(service.all())
    print('ff')