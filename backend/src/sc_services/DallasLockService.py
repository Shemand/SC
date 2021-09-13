from datetime import datetime
from sqlalchemy import update, select, delete, insert


# ----- public function
from .ServicesInterfaces import ServiceAbstract
from ..sc_repositories.DatabaseModels.ComputersTable import ComputersTable
from ..sc_entities.models import Dallas
from ..sc_repositories.DatabaseModels.DallasLockTable import DallasLockTable
from ..sc_repositories.DatabaseModels.UnitsTable import UnitsTable


class DallasLockService(ServiceAbstract):
    @staticmethod
    def _return_model_fields(row):
        return {
            "status": row['status'],
            "computer": {
                "name": row['Computers_name'],
                "unit": {
                    "name": row['Units_name'],
                }
            },
            "server": row['server'],
            "isDeleted": row['isDeleted'],
        }


    def create(self, model: Dallas):
        params = {
            "Computers_id": select([self.db.computers.c.id]).where(self.db.computers.c.name == model.computer.name).limit(1),
            "status": model.status,
            "server": model.server,
            "isDeleted": model.isDeleted
        }
        query = insert(self.db.dallas).values(**params)
        self.db.engine.execute(query)
        return True

    def delete(self, computer_name):
        query = delete(self.db.dallas).where(self.db.dallas.c.Computers_id == select([self.db.computers.c.id]).where(self.db.computers.c.name == computer_name))
        self.db.engine.execute(query)

    def get(self, computer_name):
        fields = [self.db.dallas.c.status,
                  self.db.dallas.c.server,
                  self.db.dallas.c.isDeleted,
                  self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name')]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.dallas.c.Computers_id, isouter=True)\
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True)\
            .where(self.db.computers.c.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        return Dallas(**type(self)._return_model_fields(row))

    def all(self):
        table = DallasLockTable
        fields = [self.db.dallas.c.status,
                  self.db.dallas.c.server,
                  self.db.dallas.c.isDeleted,
                  self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name')]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.dallas.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [Dallas(**type(self)._return_model_fields(row)) for row in rows]

    # ----- update computers data -----

    def update_computers_from_dallas(self, database, district):
        records_dallas = _get_dallas_computer_records(database, district)
        rows_dallas = rows_dallas = { row.Computers_id : row for row in get_dallas_computers(database) }
        _inject_row_in_computer_records(database, records_dallas, rows_dallas)
        for _, record in records_dallas.items():
            if record['dallas_row'] == None:
                record['dallas_row'] = create_computer_dallas_record(database, record['computer_row'], record)
            else:
                _update_computer_dallas_row(self, database, record['dallas_row'], record)
        for computer_id, row in rows_dallas.items():
            row.isDeleted = datetime.now()
            row.updated = datetime.now()
        database.session.commit()
        return True


    def _get_dallas_computer_records(self, database, district):
        records = {}
        for service in district.services.get_dallas_lock_services():
            records = {**records, **service.all()}
        return records


    def _inject_row_in_computer_records(self, database, records, rows_dallas):
        for computer_name, record in records.items():
            computer_row = get_or_create_computer(database, computer_name)
            record['computer_row'] = computer_row
            if computer_row.id in rows_dallas:
                record['dallas_row'] = rows_dallas[computer_row.id]
                del rows_dallas[computer_row.id]
            else:
                record['dallas_row'] = None


    def _update_computer_dallas_row(self, database, dallas_row, dallas_record):
        if dallas_row.status != dallas_record['status']:
            dallas_row.status = dallas_record['status']
        if dallas_row.server != dallas_record['server']:
            dallas_row.server = dallas_record['server']
        if dallas_row.isDeleted is not None:
            dallas_row.isDeleted = None
        return dallas_row
