from datetime import datetime
from sqlalchemy import select, delete, update, insert

from .ServicesInterfaces import ServiceAbstract
from ..sc_common.functions import delete_from_list_by_hash
from ..sc_entities.models import Kaspersky


class KasperskyService(ServiceAbstract):


    @staticmethod
    def _return_model_fields(row):
        return {
            "computer": {
                "name": row['Computers_name'],
                "unit": {
                    "name": row['Units_name'],
                }
            },
            "os": {
                "name": row['OperationSystems_name'],
                "isUnix": row['OperationSystems_isUnix']
            } if row['OperationSystems_name'] else None,
            "ip": {
                "ipv4": row['Addresses_ipv4'],
                "isAllowed": row['Addresses_isAllowed']
            } if row['Addresses_ipv4'] else None,
            "server": row['server'],
            "agent": row['agent_version'],
            "security": row['security_version'],
            "isDeleted": row['isDeleted'],
        }

    def create(self, model: Kaspersky):
        params = {
            "Computers_id": select([self.db.computers.c.id]).where(self.db.computers.name == model.computer.name).limit(1),
            "OperationSystems_id": select([self.db.os.c.id]).where(self.db.os.c.name == model.os.name).limit(1) if model.os else None,
            "Addresses_id": select([self.db.ip.c.id]).where(self.db.ip.c.ipv4 == model.ip.ipv4).limit(1) if model.ip else None,
            "agent_version": model.agent,
            "security_version": model.security,
            "server": model.server,
            "isDeleted": model.isDeleted
        }
        query = insert(self.db.kaspersky).values(**params)
        self.db.engine.execute(query)
        return True

    def delete(self, computer_name):
        query = delete(self.db.kaspersky).where(self.db.kaspersky.c.Computers_id == select([self.db.computers.c.id]).where(self.db.computers.c.name == computer_name).limit(1))
        self.db.engine.execute(query)

    def get(self, computer_name):
        fields = [self.db.kaspersky.c.server,
                  self.db.kaspersky.c.agent_version,
                  self.db.kaspersky.c.security_version,
                  self.db.kaspersky.c.isDeleted,
                  self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name'),
                  self.db.os.c.name.label('OperationSystems_name'),
                  self.db.os.c.isUnix.label('OperationSystems_isUnix'),
                  self.db.ip.c.ipv4.label('Addresses_ipv4'),
                  self.db.ip.c.isAllowed.label('Addresses_isAllowed')]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.kaspersky.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True) \
            .join(self.db.ip, self.db.ip.c.id == self.db.kapsersky.c.Addresses_id, isouter=True) \
            .join(self.db.os, self.db.os.c.id == self.db.kaspersky.c.OperationSystems_id, isouter=True) \
            .where(self.db.compuers.c.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        return Kaspersky(**type(self)._return_model_fields(row))

    def all(self):
        table = KasperskyTable
        fields = [self.db.kaspersky.c.server,
                  self.db.kaspersky.c.agent_version,
                  self.db.kaspersky.c.security_version,
                  self.db.kaspersky.c.isDeleted,
                  self.db.computers.c.name.label('Computers_name'),
                  self.db.units.c.name.label('Units_name'),
                  self.db.os.c.name.label('OperationSystems_name'),
                  self.db.os.c.isUnix.label('OperationSystems_isUnix'),
                  self.db.ip.c.ipv4.label('Addresses_ipv4'),
                  self.db.ip.c.isAllowed.label('Addresses_isAllowed')]
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.kaspersky.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True) \
            .join(self.db.ip, self.db.ip.c.id == self.db.kaspersky.c.Addresses_id, isouter=True) \
            .join(self.db.os, self.db.os.c.id == self.db.kaspersky.c.OperationSystems_id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [Kaspersky(**type(self)._return_model_fields(row)) for row in rows]

    def update_computers_from_kaspersky(self, database, district):
        kaspersky_services = district.services.get_kaspersky_services()
        kaspersky_rows = _get_kaspersky_records_from_database(database)
        records_kaspersky = {}
        updated_servers = []
        for service in kaspersky_services:
            from_service = _get_kaspersky_records_from_service(database, service)
            records_kaspersky = {**records_kaspersky, **from_service}
            updated_servers.append(service.server)
        inject_row_in_computers_records(database, records_kaspersky)
        for _, record in records_kaspersky.items():
            required_kaspersky_row = None
            for row in kaspersky_rows:
                 if row.Computers_id == record['computer'].id:
                    required_kaspersky_row = row
                    break
            if not required_kaspersky_row:
                _create_kaspersky_record(database, record['computer'], record)
            else:
                _update_kaspersky_record(database, required_kaspersky_row, record)
                delete_from_list_by_hash(kaspersky_rows, required_kaspersky_row)
        for row in kaspersky_rows:
            if row.server in updated_servers:
                row.isDeleted = datetime.now()
        database.session.commit()
        return True


    def _get_kaspersky_records_from_service(self, database, kaspersky_service):
        if kaspersky_service.check_connection():
            return kaspersky_service.all()


    def _get_kaspersky_records_from_database(self, database):
        return database.session.query(KasperskyTable).all()


    def _create_kaspersky_record(self, database, computer_row, kaspersky_record):
        params = {
            "Computers_id" : computer_row.id,
            "OperationSystems_id" : get_or_create_os(database, kaspersky_record['os']).id,
            "Addresses_id" : get_or_create_ip(database, kaspersky_record['ip']).id,
            "agent_version" : kaspersky_record['agent_version'],
            "security_version" : kaspersky_record['security_version'],
            "server" : kaspersky_record['server']
        }
        row = KasperskyTable(**params)
        database.session.add(row)
        database.session.commit()
        return row


    def _update_kaspersky_record(self, database, kaspersky_row, kaspersky_record):
        if kaspersky_row.isDeleted != None:
            kaspersky_row.isDeleted = None
        if kaspersky_row.OperationSystems_id != get_os_by_name(database, kaspersky_record['os']):
            kaspersky_row.OperationSystems_id = get_or_create_os(database, kaspersky_record['os']).id
        if kaspersky_row.Addresses_id != get_ip_by_address(database, kaspersky_record['ip']):
            kaspersky_row.Addresses_id = get_or_create_ip(database, kaspersky_record['ip']).id
        if kaspersky_row.agent_version != kaspersky_record['agent_version']:
            kaspersky_row.agent_version = kaspersky_record['agent_version']
        if kaspersky_row.security_version != kaspersky_record['security_version']:
            kaspersky_row.security_version = kaspersky_record['security_version']
        if kaspersky_row.server != kaspersky_record['server']:
            kaspersky_row.server = kaspersky_record['server']
        database.session.commit()
        return kaspersky_row


    def _delete_from_kaspersky(self, database, computer_id):
        kaspersky = database.session.query(KasperskyTable).filter_by(Computers_id=computer_id).all()
        for computer in kaspersky:
            computer.isDeleted = datetime.now()
        database.session.commit()