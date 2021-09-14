from .ServicesInterfaces import ServiceAbstract
from ..sc_common.functions import reformat_computer_name, extract_unit_from_name, reformat_unit_name
from ..sc_config.config import config
from ..sc_entities.models import Computer, ComputerBase

from sqlalchemy import select, update, delete, insert


class ComputersService(ServiceAbstract):

    @staticmethod
    def _return_model_fields(row):
        return {
            "name": row['name'],
            "unit": {
                "name": row['Units_name']
            },
            "comment": row['comment'],
        }

    def all(self):
        fields = [self.db.computers.c.name,
                  self.db.units.c.name.label('Units_name'),
                  self.db.computers.c.comment]
        query = select(fields).join(self.db.units, self.db.computers.c.Units_id == self.db.units.c.id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        computers = [Computer(**type(self)._return_model_fields(row)) for row in rows]
        return computers

    def get(self, computer_name):
        fields = [self.db.computers.c.name,
                  self.db.units.c.name.label('Units_name'),
                  self.db.computers.c.comment]
        query = select(fields) \
            .join(self.db.units, self.db.computers.c.Units_id == self.db.units.c.id, isouter=True) \
            .where(self.db.computers.c.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        computer = Computer(**type(self)._return_model_fields(row))
        return computer

    def create(self, model: ComputerBase):
        if self.is_exists(model.name):
            return False
        params = {
            "name": model.name,
            "Units_id": select([self.db.units.c.id]).where(self.db.units.c.name == model.unit.name),
        }
        if 'comment' in model.__fields__:
            params["comment"] = model.comment,
        query = insert(self.db.computers).values(**params)
        self.db.engine.execute(query)
        return True

    def update(self, model: ComputerBase):
        db_model = self.get(model.name)
        if model == db_model:
            return False
        values = {
            "Units_id" : select([self.db.units.c.id]).where(self.db.units.c.name == model.unit.name).limit(1),
            "comment": model.comment
        }
        query = update(self.db.computers).values(**values).where(self.db.computers.c.name == model.name)
        self.db.engine.execute(query)
        return True

    def delete(self, computer_name):
        query = delete(self.db.computers).where(self.db.computers.c.name == computer_name)
        self.db.engine.execute(query)

    def get_or_create(self, computer_name: str):
        computer = self.get(computer_name)
        if computer:
            return computer
        model = Computer(name=computer_name, unit={"name": config.default_unit}) # todo something units actions
        return self.create(model)

    def is_exists(self, computer_name):
        computer = self.get(computer_name)
        if computer:
            return True
        return False

    def inject_row_in_computers_records(self, database, records, name_field='name'):
        computers = {reformat_computer_name(computer.name): computer for computer in get_computers(database)}
        if isinstance(records, list):
            for record in records:
                computer_name = record[name_field]
                if not computer_name in computers:
                    computers[computer_name] = create_computer(database, computer_name)
                record['computer'] = computers[computer_name]
        elif isinstance(records, dict):
            to_remove = []
            for computer_name, d in records.items():
                computer_name = reformat_computer_name(computer_name)
                print(computer_name)
                if records[computer_name] == None:
                    to_remove.append(computer_name)
                    continue
                if not computer_name in computers:
                    computers[computer_name] = create_computer(database, computer_name)
                    records[computer_name] = computers[computer_name]
                else:
                    d['computer'] = computers[computer_name]
            for computer_name in to_remove:
                del records[computer_name]
        else:
            raise RuntimeError('computers.inject_row_in_computers_records isn\'t dict or list')

    def change_unit_name(self, database, computer_name, unit_name):
        computer = get_computer(database, computer_name)
        change_computer_unit(database, computer, unit_name)

    def change_unit_id(self, database, computer_obj, unit_name):
        if computer_obj:
            unit = get_unit_by_name(database, reformat_unit_name(unit_name))
            if unit:
                if computer_obj.Units_id != unit.id:
                    computer_obj.Units_id = unit.id
                    database.session.commit()
                return computer_obj
            print(f'change_computer_unit: Unknown unit with this name ({unit_name})')
            return None
        print(f'change_computer_unit: Unknown computer with this name ({computer_obj.name})')
        return None
