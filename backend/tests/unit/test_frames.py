from sqlalchemy import select

from backend.sc_actions.computers_frame import get_computers_frame, FROM_DALLAS_LOCK, FROM_KASPERSKY, FROM_PUPPET, FROM_ACTIVE_DIRECTORY

from backend.sc_entities.Entities import Entities


def test_computers_frames():
    district = Entities().get_district('SZO')
    database = district.database
    # frames = get_computers_frame(database, [], sources={FROM_DALLAS_LOCK : [], FROM_ACTIVE_DIRECTORY : [], FROM_KASPERSKY : [], FROM_PUPPET: []})
    frames = get_computers_frame(database, [], sources={FROM_ACTIVE_DIRECTORY: [], FROM_PUPPET: [], FROM_KASPERSKY: [], FROM_DALLAS_LOCK: []})
    print('ff')