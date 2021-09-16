from sqlalchemy import Column, Table, String, DateTime, Integer, ForeignKey, Boolean, Text
from datetime import datetime


class DBmodels():
    def __new__(cls, metadata):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBmodels, cls).__new__(cls)
            cls.instance.__initialize_tables(metadata)
        return cls.instance

    def __initialize_tables(self, metadata):
        self.users = Table('users', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('login', String(256), nullable=False, unique=True, index=True),
            Column('privileges', Integer, nullable=False, default=1),  # 0 - is blocked, 1 - is active,
            Column('created', DateTime, nullable=False, default=datetime.now()),
            Column('Users_ActiveDirectory_id', Integer, ForeignKey('active_directory_users.id')),
            Column('Units_id', Integer, ForeignKey('units.id'), nullable=False),
        )

        self.active_directory_users = Table('active_directory_users', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('name', String(64), nullable=False, index=True),
            Column('full_name', String(128), nullable=False),
            Column('department', String(128), nullable=False),
            Column('mail', String(64)),
            Column('phone', String(32)),
            Column('registred', DateTime),
            Column('last_logon', DateTime),
            Column('isDeleted', DateTime),
            Column('isDisabled', DateTime),
            Column('isLocked', DateTime),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now())
        )

        self.kaspersky = Table('kaspersky', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Computers_id', Integer, ForeignKey('computers.id'), nullable=False),
            Column('OperationSystems_id', Integer, ForeignKey('os.id')),
            Column('Addresses_id', Integer, ForeignKey('ip.id')),
            Column('agent_version', String(32)),
            Column('security_version', String(32)),
            Column('server', String(32), nullable=False),
            Column('isDeleted', DateTime),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.os = Table('os', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('name', String(64), nullable=False, unique=True),
            Column('isUnix', Boolean, nullable=False),
        )

        self.puppet_events = Table('puppet_events', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Puppets_id', Integer, ForeignKey('puppets.id'), nullable=False),
            Column('title', String(256), nullable=False, index=True),
            Column('message', Text),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.puppets = Table('puppets', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Computers_id', Integer, ForeignKey('computers.id'), nullable=False),
            Column('Addresses_id', Integer, ForeignKey('ip.id')),
            Column('OperationSystems_id', Integer, ForeignKey('os.id')),
            Column('board_serial_number', String(128)),
            Column('astra_update', String(32)),
            Column('environment', String(64), nullable=False),
            Column('domain', String(64)),
            Column('serial_number', String(128)),
            Column('isVirtual', Boolean, nullable=False, default=False),
            Column('mac', String(18)),
            Column('kesl_version', String(32)),
            Column('klnagent_version', String(32)),
            Column('uptime_seconds', Integer),
            Column('isDeleted', DateTime),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.units = Table('units', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('name', String(64), nullable=False, unique=True, default=datetime.now()),
            Column('root_id', Integer),
        )

        self.dallas = Table('dallas', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Computers_id', Integer, ForeignKey('computers.id'), nullable=False),
            Column('status', Integer, nullable=False),
            Column('server', String(64), nullable=False),
            Column('isDeleted', DateTime),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.devices = Table('devices', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Addresses_id', Integer, ForeignKey('ip.id')),
            Column('Units_id', Integer, ForeignKey('units.id'), nullable=False),
            Column('name', String(128), nullable=False),
            Column('comment', Text),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.logons = Table('logons', metadata,
            Column('Computers_id', Integer, ForeignKey('computers.id'), primary_key=True, nullable=False),
            Column('Users_id', Integer, ForeignKey('users.id'), primary_key=True, nullable=False),
            Column('OperationSystems_id', Integer, ForeignKey('os.id')),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.crypto_gateways = Table('crypto_gateways', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Units_id', Integer, ForeignKey('units.id'), nullable=False),
            Column('address', String(16), nullable=False),
            Column('mask', Integer, nullable=False),
            Column('caption', String(128), nullable=False),
            Column('name', String(5), nullable=False, index=True),
        )

        self.computers = Table('computers', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('name', String(128), nullable=False, unique=True, index=True),
            Column('comment', Text),
            Column('created', DateTime, nullable=False, default=datetime.now()),
            Column('Units_id', Integer, ForeignKey('units.id'), nullable=False),
        )

        self.active_directory_computers = Table('active_directory_computers', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Computers_id', Integer, ForeignKey('computers.id'), nullable=False),
            Column('isDeleted', DateTime),
            Column('last_visible', DateTime),
            Column('isActive', Boolean, default=True),
            Column('registred', DateTime, nullable=False),
            Column('updated', DateTime, nullable=False, default=datetime.now()),
            Column('created', DateTime, nullable=False, default=datetime.now()),
        )

        self.ip = Table('ip', metadata,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('CryptoGateways_id', Integer, ForeignKey('crypto_gateways.id')),
            Column('ipv4', String(16), nullable=False, unique=True, index=True),
            Column('isAllowed', Boolean, default=True),
        )

        self.adapters = Table('adapters', metadata,
                Column('Computers_id', Integer, ForeignKey('computers.id'), primary_key=True, nullable=False),
                Column('Users_id', Integer, ForeignKey('users.id'), primary_key=True, nullable=False),
                Column('OperationSystems_id', Integer, ForeignKey('os.id')),
                Column('created', DateTime, nullable=False, default=datetime.now()),
            )
