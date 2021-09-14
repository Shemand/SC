from .ServicesInterfaces import ServiceAbstract


class UsersService(ServiceAbstract):

    def add_user(self, database, user_name, **params):
        user_name = user_name.lower()
        user = get_user(database, user_name)
        if user:
            return user
        units_id = params.get('Units_id', None)
        if units_id is None:
            params['Units_id'] = get_default_unit(database).id
        user = UsersTable(login=user_name, **params)
        database.session.add(user)
        return user


    def get_users(self, database):
        return database.session.query(UsersTable).all()

    def get_user(database, user_name):
        user_name = user_name.lower()
        return database.session.query(UsersTable).filter_by(login=user_name).first()

    def  get_or_create_user(self, database, user_name):
        user = get_user(database, user_name)
        if user:
            return user
        user = add_user(database, user_name)
        database.session.add(user)
        database.session.commit()
        return user

    def get_user_by_id(self, database, user_id):
        return database.query(UsersTable).filter_by(id=user_id).first()


    def tangle_ad(self, database, user_id, user_ad_id):
        user = get_user_by_id(database, user_id)
        if user:
            ad_user = database.session.query(Users_ActiveDirectoryTable).fiter_by(id=user_ad_id).first()
            ad_user.Users_id = user_id
            database.session.commit()
            return user
        return None


    def change_privileges(self, database, user_id, role_number):
        user = get_user_by_id(database, user_id)
        if user:
            user.privileges = role_number
            database.session.commit()
            return user
        return None

    def inject_row_in_users_records(self, database, records, name_field='account_name'):
        users = { user.login : user for user in get_users(database) }
        if isinstance(records, list):
            for record in records:
                user_name = record[name_field]
                if not user_name in users:
                    users[user_name] = add_user(database, user_name)
                record['user'] = users[user_name]
        elif isinstance(records, dict):
            for user_name, d in records.items():
                if not user_name in users:
                    users[user_name] = add_user(database, user_name)
                d['user'] = users[user_name]
        else:
            raise RuntimeError('users.inject_row_in_users_records isn\'t dict or list')
