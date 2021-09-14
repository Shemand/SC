from datetime import datetime

from sqlalchemy import select, insert, update
# ----- public function
from .ServicesInterfaces import ServiceAbstract
from ..sc_entities.models import Puppet


class UpdatePuppetComputers(ServiceAbstract):
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
            "board_serial": row['board_serial'],
            "astra_update": row['astra_update'],
            "environment": row['environment'],
            "domain": row['domain'],
            "serial_number": row['serial_number'],
            "isVirtual": row['isVirtual'],
            "mac": row['mac'],
            "kesl": row['kesl_version'],
            "kl_agent": row['klnagent_version'],
            "update_seconds": row['update_secords'],
            "isDeleted": row['isDeleted'],
        }

    def _return_db_fields(self):
        return [self.db.puppets.c.board_serial_number,
                self.db.puppets.c.astra_update,
                self.db.puppets.c.environment,
                self.db.puppets.c.domain,
                self.db.puppets.c.serial_number,
                self.db.puppets.c.isVirtual,
                self.db.puppets.c.mac,
                self.db.puppets.c.kesl_version,
                self.db.puppets.c.klnagent_version,
                self.db.puppets.c.uptime_seconds,
                self.db.puppets.c.isDeleted,
                self.db.computers.c.name.label('Computers_name'),
                self.db.units.c.name.label('Units_name'),
                self.db.os.c.name.label('OperationSystems_name'),
                self.db.os.c.isUnix.label('OperationSystems_isUnix'),
                self.db.ip.c.ipv4.label('Addresses_ipv4'),
                self.db.ip.c.isAllowed.label('Addresses_isAllowed')]


    def create(self, model: Puppet):
        params = {
            "Computers_id": select([self.db.computers.c.id]).where(self.db.computers.name == model.computer.name).limit(1),
            "OperationSystems_id": self.db.get_id_os(model.os.name) if model.os else None,
            "Addresses_id": self.db.get_id_ip(model.ip.ipv4) if model.ip else None,
            "board_serial": model.board_serial,
            "astra_update": model.astra_update,
            "environment": model.environment,
            "domain": model.domain,
            "serial_number": model.serial_number,
            "isVirtual": model.isVirtual,
            "mac": model.mac,
            "kesl_version": model.kesl,
            "klnagent_version": model.klnagent,
            "update_seconds": model.update_seconds,
            "isDeleted": model.isDeleted,
        }
        query = insert(self.db.puppets).values(**params)
        self.db.engine.execute(query)
        return True

    def delete(self, computer_name):
        query = update(self.db.puppets).values(isDeleted=datetime.now()) \
            .join(self.db.computers, self.db.computers.c.id == self.db.puppets.c.Computers_id, isouter=True)\
            .where(self.db.computers.c.name == computer_name)
        self.db.engine.execute(query)

    def recovery(self, computer_name):
        query = update(self.db.puppets).values(isDeleted=None)\
            .join(self.db.computers, self.db.computers.c.id == self.db.puppets.c.Computers_id, isouter=True)\
            .where(self.db.computers.c.name == computer_name)
        self.db.engine.execute(query)

    def get(self, computer_name):
        fields = self._return_db_fields()
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.puppets.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True) \
            .join(self.db.ip, self.db.ip.c.id == self.db.kapsersky.c.Addresses_id, isouter=True) \
            .join(self.db.os, self.db.os.c.id == self.db.kaspersky.c.OperationSystems_id, isouter=True) \
            .where(self.db.computers.c.name == computer_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        return Puppet(**type(self)._return_model_fields(row))

    def all(self):
        fields = self._return_db_fields()
        query = select(fields) \
            .join(self.db.computers, self.db.computers.c.id == self.db.puppets.c.Computers_id, isouter=True) \
            .join(self.db.units, self.db.units.c.id == self.db.computers.c.Units_id, isouter=True) \
            .join(self.db.ip, self.db.ip.c.id == self.db.kaspersky.c.Addresses_id, isouter=True) \
            .join(self.db.os, self.db.os.c.id == self.db.kaspersky.c.OperationSystems_id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [Puppet(**type(self)._return_model_fields(row)) for row in rows]

    def get_puppet_computers(database):
        return database.session.query(PuppetsTable).all()


    def create_computer_puppet_record(database, record):
        params = {
            "Computers_id": record['computer_row'].id,
            "Addresses_id": record['ip_row'].id if record['ip_row'] else None,
            "OperationSystems_id": record['os_row'].id if record['os_row'] else None,
            "board_serial_number": record['boardserialnumber'],
            "astra_update": record['astra_update_version'],
            "environment": record['environment'],
            "domain": record['domain'],
            "serial_number": record['serial_number'],
            "isVirtual": record['is_virtual'],
            "mac": record['macaddress'],
            "kesl_version": record['kesl_astra_version'],
            "klnagent_version": record['klnagent_astra_version'],
            "uptime_seconds": record['uptime_seconds']
        }
        row = PuppetsTable(**params)
        database.session.add(row)
        # database.session.commit()
        return row

    # ----- update computers data -----


    def update_computers_from_puppet(database, district):
        records_puppet = _get_puppet_records(database, district)
        rows_puppet = { row.Computers_id : row for row in get_puppet_computers(database) }
        _inject_rows_in_records(database, records_puppet)
        for _, record in records_puppet.items():
            puppet_row = rows_puppet.get(record['computer_row'].id, None)
            if puppet_row is not None:
                del rows_puppet[record['computer_row'].id]
                _update_puppet_row(database, puppet_row, record)
            else:
                create_computer_puppet_record(database, record)
        for computer_id, row in rows_puppet.items():
            row.isDeleted = datetime.now()
            row.updated = datetime.now()
        database.session.commit()
        return True


    def _get_puppet_records(database, district):
        records = {}
        for service in district.services.get_puppet_services():
            records = {**records, **service.all()}
        return records


    def _update_puppet_row(database, puppet_row, puppet_record):
        ip_row_id = puppet_record['ip_row'].id if puppet_record['ip_row'] else None
        os_row_id = puppet_record['os_row'].id if puppet_record['os_row'] else None
        if puppet_row.Computers_id != puppet_record['computer_row'].id:
            puppet_row.Computers_id = puppet_record['computer_row'].id
        if puppet_row.Addresses_id != ip_row_id:
            puppet_row.Addresses_id = ip_row_id
        if puppet_row.OperationSystems_id != os_row_id:
            puppet_row.OperationSystems_id = os_row_id
        if puppet_row.board_serial_number != puppet_record['boardserialnumber']:
            puppet_row.board_serial_number = puppet_record['boardserialnumber']
        if puppet_row.astra_update != puppet_record['astra_update_version']:
            puppet_row.astra_update = puppet_record['astra_update_version']
        if puppet_row.environment != puppet_record['environment']:
            puppet_row.environment = puppet_record['environment']
        if puppet_row.domain != puppet_record['domain']:
            puppet_row.domain = puppet_record['domain']
        if puppet_row.serial_number != puppet_record['serial_number']:
            puppet_row.serial_number = puppet_record['serial_number']
        if puppet_row.isVirtual != puppet_record['is_virtual']:
            puppet_row.isVirtual = puppet_record['is_virtual']
        if puppet_row.mac != puppet_record['macaddress']:
            puppet_row.mac = puppet_record['macaddress']
        if puppet_row.kesl_version != puppet_record['kesl_astra_version']:
            puppet_row.kesl_version = puppet_record['kesl_astra_version']
        if puppet_row.klnagent_version != puppet_record['klnagent_astra_version']:
            puppet_row.klnagent_version = puppet_record['klnagent_astra_version']
        if puppet_row.uptime_seconds != puppet_record['uptime_seconds']:
            puppet_row.uptime_seconds = puppet_record['uptime_seconds']
        if puppet_row.isDeleted != None:
            puppet_row.isDeleted = None

        return puppet_row

    def _inject_rows_in_records(database, records_puppet):
        for computer_name, record in records_puppet.items():
            __inject_computer_in_records(database, record, computer_name)
            __inject_ip_in_records(database, record)
            __inject_os_in_records(database, record)

    def __inject_computer_in_records(database, record, computer_name):
        record['computer_row'] = get_or_create_computer(database, computer_name)

    def __inject_os_in_records(database, record):
        if 'os' in record and record['os']:
            if 'distro' in record['os'] and 'description' in record['os']['distro']:
                os_name = record['os']['name'] + ' ' + record['os']['distro']['description']
            else:
                os_name = record['os']['name']
            record['os_row'] = get_or_create_os(database, os_name)
        else:
            record['os_row'] = None

    def __inject_ip_in_records(database, record):
        if 'ipaddress' in record and record['ipaddress']:
            record['ip_row'] = get_or_create_ip(database, record['ipaddress'])
        else:
            record['ip_row'] = None
