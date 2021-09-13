from datetime import datetime

from .ServicesInterfaces import ServiceAbstract
from ..sc_common.functions import delete_from_list_by_hash
from ..sc_common.functions import reformat_computer_name
from ..sc_entities.models import ADUser, ADComputer
from ..sc_repositories.DatabaseModels.Computers import Computers
from ..sc_repositories.DatabaseModels.Computers_ActiveDirectory import Computers_ActiveDirectory
from ..sc_repositories.DatabaseModels.Units import Units
from ..sc_repositories.DatabaseModels.Users_ActiveDirectory import Users_ActiveDirectory

from sqlalchemy import select, update, insert


class ActiveDirectoryService(ServiceAbstract):

    @staticmethod
    def _return_user_fields(row):
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

    @staticmethod
    def _return_computer_fields(row):
        return {
            "computer": {
                "name": row['Computers_name'],
                "unit": {
                    "name": row['Units_name'],
                }
            },
            "isActive": row['isActive'],
            "registred": row['registred'],
            "last_visible": row['last_visible'],
            "isDeleted": row['isDeleted'],
        }

    # -- users
    def get_user(self, user_name):
        columns = Users_ActiveDirectory
        fields = [columns.name, columns.full_name, columns.department, columns.mail, columns.phone, columns.registred,
                  columns.last_logon, columns.isDeleted, columns.isDisabled, columns.isLocked]
        query = select(fields).where(columns.name == user_name)
        row = self.db.engine.execute(query).fetchone()
        return ADUser(**type(self)._return_user_fields(row))

    def all_users(self):
        columns = Users_ActiveDirectory
        fields = [columns.name, columns.full_name, columns.department, columns.mail, columns.phone, columns.registred,
                  columns.last_logon, columns.isDeleted, columns.isDisabled, columns.isLocked]
        query = select(fields)
        users = [ADUser(**type(self)._return_user_fields(row)) for row in self.db.engine.execute(query)]
        return users

    # -- computers
    def delete_computer(self, computer_name):
        ad_table = Computers_ActiveDirectory
        query = update(ad_table).values(isDeleted=datetime.now()) \
            .where(ad_table.c.name == select(Computers.c.name)
                   .where(Computers.c.name == computer_name).limit(1))
        self.db.engine.execute(query)

    def create_computer(self, ad_model):
        params = {
            "name" : select([Computers.name.label('name')]).where(Computers.name == ad_model['name']).limit(1),
            "isDeleted" : ad_model['isDeleted'],
            "last_visible" : ad_model['last_visible'],
            "isActive" : ad_model['isActive'],
            "registred" : ad_model['registred'],
        }
        query = insert(Computers_ActiveDirectory).values(**params)
        self.db.engine.execute(query)
        return True

    def get_computer(self, computer_name):
        table = Computers_ActiveDirectory
        fields = [Computers.name.label('Computers_name'), Units.name.label('Units_name'), table.isDeleted, table.last_visible, table.isActive, table.registred]
        query = select(fields) \
            .join(Computers, Computers.id == Computers_ActiveDirectory.Computers_id, isouter=True)\
            .join(Units, Computers.Units_id == Units.id, isouter=True)\
            .where(Computers.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        return ADComputer(**type(self)._return_computer_fields(row))

    def all_computers(self):
        table = Computers_ActiveDirectory
        fields = [Computers.name.label('Computers_name'), Units.name.label('Units_name'), table.isDeleted, table.last_visible, table.isActive, table.registred]
        query = select(fields) \
            .join(Computers, Computers.id == Computers_ActiveDirectory.Computers_id, isouter=True) \
            .join(Units, Computers.Units_id == Units.id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [ADComputer(**type(self)._return_computer_fields(row)) for row in rows]

    def create_user(self, ad_model):
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

    def update(self):
        ad_services = self.repos
        ad_rows = self.get_all_computers_rows(database)
        records_ad = []
        for service in ad_services:
            records_ad.extend(_get_ad_computer_records(database, service))
        inject_row_in_computers_records(database, records_ad)
        for record in records_ad:
            required_ad_row = None
            for row in ad_rows:
                if row.Computers_id == record['computer'].id \
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

    def _get_ad_computer_records(self, database, ad_service):
        if ad_service.check_connection():
            return ad_service.all()

    def _get_ad_computers_rows(self, database):
        return database.session.query(Computers_ActiveDirectory).all()

    def _update_computer_ad_record(self, database, ad_row, ad_record):
        if ad_row.last_visible != ad_record['last_logon']:
            ad_row.last_visible = ad_record['last_logon']
        if not ad_row.isActive != ad_record['disabled']:
            ad_row.isActive = not ad_record['disabled']
        # database.session.commit()
        return ad_row

    def _computer_ad_record_in_list(self, database, ad_records, computer_row):
        for ad_record in ad_records:
            if computer_row.name == ad_record.name:
                if computer_row['last_visible'] == ad_record['last_logon']:
                    return ad_record
        return None

    # ----- update ad users -----

    def update_users_from_ad(self, database, district):
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
