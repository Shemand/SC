from backend.sc_database.model.Addresses import Addresses


def get_ip_all(database):
    ip_addresses = database.session.query(Addresses).all()
    return ip_addresses


def get_ip_by_address(database, ip):
    ip = database.session.query(Addresses).filter_by(ipv4=str(ip)).first()
    if not ip:
        return None
    return ip

def get_ip_by_id(database, ip_id):
    ip = database.session.query(Addresses).filter_by(id=ip_id).first()
    if not ip:
        return None
    return ip


def create_ip(database, ip):
    params = {
        "CryptoGateways_id": get_cg_by_ip(database, ip),
        "ipv4": ip
    }
    ip = Addresses(**params)
    database.session.add(ip)
    database.commit()
    return ip


def get_or_create_ip(database, ip):
    ip_address = get_ip_by_address(database, ip)
    if ip_address:
        return ip_address
    return create_ip(database, ip)


def is_exists_ip(database, ip_address):
    ip_address = get_ip_by_address(database, ip_address)
    if ip_address:
        return True
    return False


def get_cg_by_ip(database, ip): # todo
    return None