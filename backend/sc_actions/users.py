from backend.sc_database.model.Users import Users
from backend.sc_database.model.Users_ActiveDirectory import Users_ActiveDirectory


def add_user(database, user_name, **params):
    user = get_user(database, user_name)
    if user:
        return None
    user = Users(name=user_name, **params)
    database.session.add(user)
    return get_user(database, user_name)


def get_user(database, user_name):
    return database.query(Users).filter_by(name=user_name).first()


def get_user_by_id(database, user_name):
    return database.query(Users).filter_by(name=user_name).first()


def tangle_ad(database, user_id, user_ad_id):
    user = get_user_by_id(database, user_id)
    if user:
        ad_user = database.session.query(Users_ActiveDirectory).fiter_by(id=user_ad_id).first()
        ad_user.Users_id = user_id
        database.session.commit()
        return user
    return None


def change_privileges(database, user_id, role_number):
    user = get_user_by_id(database, user_id)
    if user:
        user.privileges = role_number
        database.session.commit()
        return user
    return None