from datetime import datetime

from backend.src.sc_entities.models import CryptoGateway, Dallas, Ip, Kaspersky, User, Unit
from backend.src.sc_entities.models import ADUser, ADComputer, Computer
from backend.src.sc_services.ComputersActiveDirectoryService import ComputersActiveDirectoryService
from backend.src.sc_services.ComputersService import ComputersService
from backend.src.sc_services.CryptoGatewaysService import CryptoGatewaysService
from backend.src.sc_services.DallasLockService import DallasLockService
from backend.src.sc_services.KasperskyService import KasperskyService
from backend.src.sc_services.UsersActiveDirectoryService import UsersActiveDirectoryService
from backend.src.sc_services.UsersService import UsersService


def test_database_repository_functions(test_database_repository):
    test_database_repository.get_ip('10.3.128.160')
    test_database_repository.get_os('Azure')

def test_users_active_directory_service(test_database_repository):
    db = test_database_repository
    ad_service = UsersActiveDirectoryService([], db)

    user = ad_service.get('shemakovnd')
    assert isinstance(user, ADUser), "Cannot find user"

    users = ad_service.all()


def test_computers_active_directory_service(test_database_repository):
    db = test_database_repository
    ad_service = ComputersActiveDirectoryService([], db)

    computer = ad_service.get('SZO-555-1015')
    assert isinstance(computer, ADComputer), "Cannot find computer"

    computers = ad_service.all()
    print('ff')


def test_computers_service(test_database_repository):
    db = test_database_repository
    service = ComputersService([], db)
    computer_name = 'SZO-XXX-0000'
    # if service.is_exists(computer_name):
    #     service.delete(computer_name)

    computer = Computer(name=computer_name, comment='All done.', unit={"name": "SZO"})
    status = service.create(computer)

    computer = service.get('SZO-555-1015')
    assert isinstance(computer, Computer), "Cannot find computer"

    computers = service.all()
    # service.delete(computer_name)
    # assert not service.is_exists(computer_name), 'Computer wasn\'t deleted'

def test_cg_service(test_database_repository):
    db = test_database_repository
    service = CryptoGatewaysService([], db)
    name = "58293"
    model = CryptoGateway(**{
        "name": name,
        "caption": "Тестовый криптошлюз",
        "address": "10.3.240.0",
        "mask": 24,
        "unit": {
            "name": "SZO"
        },
    })
    cg = service.get(name)
    if cg:
        service.delete(name)

    status = service.create(model)
    assert status, 'CryptoGateway doesn\'t create'

    cg = service.get(name)
    assert isinstance(cg, CryptoGateway), "Cannot find CryptoGateway"


    crypto_gateways = service.all()
    service.delete(name)

def test_dallas_service(test_database_repository):
    db = test_database_repository
    service = DallasLockService([], db)
    computer_name = 'SZO-XXX-0000'
    model = Dallas(**{
        "status": 5,
        "server": "vch",
        "isDeleted": datetime.now(),
        "computer": {
            "name": computer_name,
            "unit": {
                "name": "SZO"
            },
        },
    })
    dallas = service.get(computer_name)
    if dallas:
        service.delete(computer_name)

    status = service.create(model)
    assert status, 'Dallas doesn\'t create'

    dallas = service.get(computer_name)
    assert isinstance(dallas, Dallas), "Cannot find Dallas"


    dallases = service.all()
    service.delete(computer_name)

#
# def test_ip_service(test_database_repository):
#     db = test_database_repository
#     service = IpService([], db)
#     ipv4 = '172.21.21.2'
#     if service.is_exists(ipv4):
#         service.delete(ipv4)
#
#     ip = Ip(ipv4=ipv4, isAllowed=None)
#     status = service.create(ip)
#     assert status, 'IP doesn\'t create'
#
#     ip = service.get(ipv4)
#     assert isinstance(ip, Ip), "Cannot find computer"
#
#     ip = service.all()


def test_kaspersky_service(test_database_repository):
    db = test_database_repository
    service = KasperskyService([], db)
    computer_name = 'SZO-XXX-0000'

    if service.get(computer_name):
        service.delete(computer_name)

    model = Kaspersky(**{
        "computer": {
            "name": computer_name,
            "unit": {
                "name": "SZO"
            },
        },
        "os": {
            "name": "AstraLinux",
            "isUnix": True,
        },
        "ip": {
            "ipv4": "192.168.0.12",
            "isAllowed": True,
        },
        "agent": "11.1.1.1",
        "security": "11.0.0.1",
        "server": "SZO",
        "isDeleted": datetime.now(),
    })
    kaspersky = service.get(computer_name)
    if kaspersky:
        service.delete(computer_name)

    status = service.create(model)
    assert status, 'Kaspersky doesn\'t create'

    kaspersky = service.get(computer_name)
    assert isinstance(kaspersky, Kaspersky), "Cannot find Kaspersky"


    kapserskies = service.all()
    service.delete(computer_name)


def test_users_service(test_database_repository):
    db = test_database_repository
    service = UsersService([], db)
    ad_service = UsersActiveDirectoryService([], db)
    user_name = 'tsarievae'
    # if service.is_exists(computer_name):
    #     service.delete(computer_name)


    ad_user = ad_service.get(user_name)
    unit = Unit(name='SZO')
    user = User(login=user_name, privileges=1, ad=ad_user, unit=unit)
    status = service.create(user)

    # service.delete(computer_name)
    # assert not service.is_exists(computer_name), 'Computer wasn\'t deleted'
