from datetime import datetime

from sqlalchemy import select, and_, or_
from sqlalchemy.testing import in_

from ..sc_repositories.DatabaseModels.AddressesTable import AddressesTable
from ..sc_repositories.DatabaseModels.ComputersTable import ComputersTable
from ..sc_repositories.DatabaseModels.Computers_ActiveDirectory import Computers_ActiveDirectory
from ..sc_repositories.DatabaseModels.PuppetsTable import PuppetView
from ..sc_repositories.DatabaseModels.KasperskyTable import  KasperskyView
from ..sc_repositories.DatabaseModels.DallasLockTable import DallasLockTable
from ..sc_repositories.DatabaseModels.UnitsTable import UnitsTable

""""

units - list of units with how row will be returned
sources - if a dict with fields. Values = {
    "puppet" : ["ip", "os", "board_serial", "astra_update", "environment", "domain", "serial_number", "isVirtual",
                "mac", "kesl_vesion", "klnagent_version", "uptime_seconds", "isDeleted", "updated", "created"],
    "kaspersky" : ["os", "ip", "agent_version", "security_verison", "server", "isDeleted", "updated", "created"],
    "active_directory" : ["isDeleted", "last_visible", "isActive", "registred", "updated", "created"],
    "dallas_lock" : ["status", "server", "isDeleted", "updated", "created"]
}, another values will be skipped

"""


FROM_PUPPET = 'puppet'
FROM_KASPERSKY = 'kaspersky'
FROM_ACTIVE_DIRECTORY ='active_directory'
FROM_DALLAS_LOCK = 'dallas_lock'

MAIN_FIELDS = {
    "id" : ComputersTable.id,
    "name" : ComputersTable.name,
    "comment" : ComputersTable.comment,
    "created": ComputersTable.created,
    "unit": UnitsTable.name.label('unit')
}

SOURCES = {
    FROM_PUPPET: {
        "puppet_ip": PuppetView.puppet_ip,
        "puppet_os": PuppetView.puppet_os,
        "board_serial_number": PuppetView.board_serial_number,
        "astra_update": PuppetView.astra_update,
        "environment": PuppetView.environment,
        "domain": PuppetView.domain,
        "serial_number": PuppetView.serial_number,
        "isVirtual": PuppetView.isVirtual,
        "mac": PuppetView.mac,
        "kesl_version": PuppetView.kesl_version,
        "klnagent_version": PuppetView.klnagent_version,
        "uptime_seconds": PuppetView.uptime_seconds,
        "isDeleted": PuppetView.isDeleted,
        "puppet_updated": PuppetView.updated.label('puppet_updated'),
        "puppet_created": PuppetView.created.label('puppet_created')
    },
    FROM_KASPERSKY: {
        "kl_os": KasperskyView.kl_os,
        "kl_ip": KasperskyView.kl_ip,
        "agent_version": KasperskyView.agent_version,
        "security_version": KasperskyView.security_version,
        "server": KasperskyView.server,
        "isDeleted": KasperskyView.isDeleted,
        "kl_updated": KasperskyView.updated.label('kl_updated'),
        "kl_created": KasperskyView.created.label('kl_created')
    },
    FROM_DALLAS_LOCK: {
        "status": DallasLockTable.status,
        "server": DallasLockTable.server,
        "isDeleted": DallasLockTable.isDeleted,
        "dl_updated": DallasLockTable.updated.label('dl_updated'),
        "dl_created": DallasLockTable.created.label('dl_created')
    },
    FROM_ACTIVE_DIRECTORY: {
        "isDeleted": Computers_ActiveDirectory.isDeleted,
        "last_visible": Computers_ActiveDirectory.last_visible,
        "isActive": Computers_ActiveDirectory.isActive,
        "registred": Computers_ActiveDirectory.registred,
        "ad_updated": Computers_ActiveDirectory.updated.label('ad_updated'),
        "ad_created": Computers_ActiveDirectory.created.label('ad_created')
    }
}

def get_computers_frame(database, units, sources=[], with_fields=[ComputersTable]):
    from_tables = ComputersTable.__table__
    query = select(_build_select(sources))
    sources_names = [source_name for source_name in sources]
    query = query.select_from(_build_from(sources))
    where_expression = UnitsTable.id.in_(units)
    if where_expression is not None:
        query = query.where(where_expression)
    computers = database.engine.execute(query)
    records = []
    for computer in computers:
        records.append(_format_record(computer, sources))
    return records


def _format_record(computer, sources):
    record = {}
    for field_name in MAIN_FIELDS: # fill base params in record
        record[field_name] = computer[field_name]
    for source_name, source_fields in sources.items(): # fill another sources in record
        if source_fields == []:
            source_fields = [sf for sf in SOURCES[source_name]]
        record[source_name] = {}
        for source_field in source_fields:
            record[source_name][source_field] = computer[source_field]
    return record


def _build_select(sources):
    global field_name
    fields = [field for _, field in MAIN_FIELDS.items()]
    for source_name, source_fields in sources.items():
        if not source_name in SOURCES:
            continue
        if source_fields != []:
            fields.extend([ SOURCES[source_name][field_name] for field_name in source_fields if field_name in SOURCES[source_name] ])
        else:
            fields.extend([ SOURCES[source_name][field_name] for field_name in SOURCES[source_name] ])
    return fields


def _build_from(sources):
    from_tables = ComputersTable.__table__

    for source in sources:
        if not source in SOURCES:
            continue
        if source == FROM_PUPPET:

            from_tables = from_tables.join(PuppetView, ComputersTable.id == PuppetView.Computers_id, isouter=True)
        if source == FROM_DALLAS_LOCK:
            from_tables = from_tables.join(DallasLockTable, ComputersTable.id == DallasLockTable.Computers_id, isouter=True)
        if source == FROM_ACTIVE_DIRECTORY:
            from_tables = from_tables.join(Computers_ActiveDirectory, ComputersTable.id == Computers_ActiveDirectory.Computers_id, isouter=True)
        if source == FROM_KASPERSKY:
            from_tables = from_tables.join(KasperskyView, ComputersTable.id == KasperskyView.Computers_id, isouter=True)
    from_tables = from_tables.join(UnitsTable, ComputersTable.Units_id == UnitsTable.id, isouter=True)
    return from_tables
