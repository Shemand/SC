from datetime import datetime

from sqlalchemy import select, and_, or_
from sqlalchemy.testing import in_

from ..sc_database.model.Units import Units
from ..sc_database.model.Users import Users
from ..sc_database.model.Users_ActiveDirectory import Users_ActiveDirectory

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


FROM_LOCAL = 'local'
FROM_ACTIVE_DIRECTORY ='active_directory'

MAIN_FIELDS = {
}

SOURCES = {
    FROM_LOCAL: {
        "login": Users.login,
        "privileges": Users.privileges,
        "created": Users.created,
        "Users_ActiveDirectory_id": Users.Users_ActiveDirectory_id.label('dl_updated'),
        "Units_id": Users.Units_id.label('dl_created')
    },
    FROM_ACTIVE_DIRECTORY: {
        "name": Users_ActiveDirectory.name,
        "full_name": Users_ActiveDirectory.full_name,
        "department": Users_ActiveDirectory.department,
        "mail": Users_ActiveDirectory.mail,
        "phone": Users_ActiveDirectory.phone,
        "registred": Users_ActiveDirectory.registred,
        "last_logon": Users_ActiveDirectory.last_logon,
        "isDeleted": Users_ActiveDirectory.isDeleted,
        "isDisabled": Users_ActiveDirectory.isDisabled,
        "isLocked": Users_ActiveDirectory.isLocked,
        "updated": Users_ActiveDirectory.updated.label('ad_updated'),
        "created": Users_ActiveDirectory.created.label('ad_created'),
    }
}

def get_computers_frame(database, units, sources=[], with_fields=[Users]):
    from_tables = Users.__table__
    query = select(_build_select(sources))
    sources_names = [source_name for source_name in sources]
    query = query.select_from(_build_from(sources))
    where_expression = Units.id.in_(units)
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
    from_tables = Computers.__table__

    for source in sources:
        if not source in SOURCES:
            continue
        if source == FROM_PUPPET:

            from_tables = from_tables.join(PuppetView, Computers.id == PuppetView.Computers_id, isouter=True)
        if source == FROM_DALLAS_LOCK:
            from_tables = from_tables.join(DallasLock, Computers.id == DallasLock.Computers_id, isouter=True)
        if source == FROM_ACTIVE_DIRECTORY:
            from_tables = from_tables.join(Computers_ActiveDirectory, Computers.id == Computers_ActiveDirectory.Computers_id, isouter=True)
        if source == FROM_KASPERSKY:
            from_tables = from_tables.join(KasperskyView, Computers.id == KasperskyView.Computers_id, isouter=True)
    from_tables = from_tables.join(Units, Computers.Units_id == Units.id, isouter=True)
    return from_tables
