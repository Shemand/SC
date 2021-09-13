from datetime import datetime

from sqlalchemy import select, update, insert

from backend.src.sc_entities.models import ADUser
from backend.src.sc_repositories.DatabaseModels.Users_ActiveDirectoryTable import Users_ActiveDirectoryTable
from backend.src.sc_services.ServicesInterfaces import ServiceAbstract


class UsersActiveDirectoryService(ServiceAbstract):

    @staticmethod
    def _return_model_fields(row):
        return {
            "name": row['name'],
            "full_name": row['full_name'],
            "department": row['department'],
            "mail": row['mail'],
            "phone": row['phone'],
            "registred": row['registred'],
            "last_logon": row['last_logon'],
            "isDeleted": row['isDeleted'],
            "isDisabled": row['isDisabled'],
            "isLocked": row['isLocked']
        }

    # -- users
    def get(self, user_name):
        columns = Users_ActiveDirectoryTable
        fields = [columns.name, columns.full_name, columns.department, columns.mail, columns.phone, columns.registred,
                  columns.last_logon, columns.isDeleted, columns.isDisabled, columns.isLocked]
        query = select(fields).where(columns.name == user_name)
        row = self.db.engine.execute(query).fetchone()
        return ADUser(**type(self)._return_model_fields(row))

    def all(self):
        columns = Users_ActiveDirectoryTable
        fields = [columns.name, columns.full_name, columns.department, columns.mail, columns.phone, columns.registred,
                  columns.last_logon, columns.isDeleted, columns.isDisabled, columns.isLocked]
        query = select(fields)
        users = [ADUser(**type(self)._return_model_fields(row)) for row in self.db.engine.execute(query)]
        return users

    def create(self, ad_model):
        params = {
            "name": ad_model.name,
            "full_name": ad_model.full_name,
            "department": ad_model.department,
            "mail": ad_model.mail,
            "phone": ad_model.phone,
            "registred": ad_model.whenCreated,
            "last_logon": ad_model.last_logon,
            "isDisabled": datetime.now() if ad_model.disabled else None,
            "isLocked": datetime.now() if ad_model.locked else None
        }
        query = insert().value(**params)
        self.db.engine.execute(query)
        return True

    def update(self, database, district):
        ad_services = district.services.get_active_directory_services()
        ad_rows = get_ad_users(database)
        records_ad = []
        for service in ad_services:
            records_ad.extend(_get_ad_users_records(database, service))
        inject_row_in_users_records(database, records_ad)
        for record in records_ad:
            required_ad_row = None
            for row in ad_rows:
                if row.login == record['computer'].id \
                        and row.registred == record['whenCreated']:
                    required_ad_row = row
                    break
            if not required_ad_row:
                create_computer_ad_record(database, record['computer'], record)
            else:
                _update_computer_ad_record(database, required_ad_row, record)
                delete_from_list_by_hash(ad_rows, required_ad_row)
        for row in ad_rows:
            row.isDeleted = datetime.now()
        database.session.commit()
        return True

    def _get_ad_users_records(self, database, ad_service):
        if ad_service.check_connection():
            return ad_service.get_users()

    def _update_user_ad_row(self, record):
        row = record['ad_row']
        if record['user_row'] is not None \
                and record['user_row'].Users_ActiveDirectory_id != row.id:
            record['user_row'].Users_ActiveDirectory_id = row.id
        if row.isDeleted is not None:
            row.isDeleted = None
        if record['name'] != row.full_name:
            row.full_name = record['name']
        if record['account_name'] != row.name:
            row.name = record['account_name']
        if record['last_logon'] != row.last_logon:
            row.last_logon = record['last_logon']
        if record['mail'] != row.mail:
            row.mail = record['mail']
        if record['phone'] != row.phone:
            row.phone = record['phone']
        if record['department'] != row.department:
            row.department = record['department']
        if record['locked'] and row.isLocked is None:
            row.isLocked = datetime.now()
        elif row.isLocked and not record['locked']:
            row.isLocked = None
        if record['disabled'] and row.isDisabled is None:
            row.isDisabled = datetime.now()
        elif row.isDisabled and not record['disabled']:
            row.isDisabled = None
