from datetime import datetime

from .ServicesInterfaces import ServiceAbstract
from ..sc_common.functions import delete_from_list_by_hash
from ..sc_common.functions import reformat_computer_name
from ..sc_entities.models import ADUser, ADComputer

from sqlalchemy import select, update, insert


class ComputersActiveDirectoryService(ServiceAbstract):

    @staticmethod
    def _return_model_fields(row):
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

    def delete(self, computer_name):
        query = update(self.db.ad_computers).values(isDeleted=datetime.now()) \
            .where(self.db.ad_computers.c.name == select(self.db.computers.c.id)
                   .where(self.db.computers.c.name == computer_name).limit(1))
        self.db.engine.execute(query)

    def recovery(self, computer_name):
        query = update(self.db.ad_computers).values(isDeleted=None) \
            .where(self.db.ad_computers.c.name == select(self.db.computers.c.id)
                   .where(self.db.computers.c.name == computer_name).limit(1))
        self.db.engine.execute(query)

    def create(self, ad_model):
        params = {
            "name": select([self.db.computers.c.name.label('name')])
                .where(self.db.computers.c.name == ad_model['name']).limit(1),
            "isDeleted" : ad_model['isDeleted'],
            "last_visible" : ad_model['last_visible'],
            "isActive" : ad_model['isActive'],
            "registred" : ad_model['registred'],
        }
        query = insert(self.db.ad_computers).values(**params)
        self.db.engine.execute(query)
        return True

    def get(self, computer_name):
        fields = [self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name'),
                  self.db.ad_computers.c.isDeleted,
                  self.db.ad_computers.c.last_visible,
                  self.db.ad_computers.c.isActive,
                  self.db.ad_computers.c.registred]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.ad_computers.c.Computers_id, isouter=True)\
            .join(self.db.units, self.db.computers.c.Units_id == self.db.units.c.id, isouter=True)\
            .where(self.db.computers.c.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return row
        return ADComputer(**type(self)._return_model_fields(row))

    def all(self):
        fields = [self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name'),
                  self.db.ad_computers.c.isDeleted,
                  self.db.ad_computers.c.last_visible,
                  self.db.ad_computers.c.isActive,
                  self.db.ad_computers.c.registred]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.ad_computers.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.computers.c.Units_id == self.db.units.c.id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [ADComputer(**type(self)._return_model_fields(row)) for row in rows]


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
