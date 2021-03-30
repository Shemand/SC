from backend.sc_entities.Entities import Entities


class User:
    def __init__(self, name=None, id=None):
        self._name = None
        self._district = None
        self._id = None
        self._object = None

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def district(self):
        return self._district

    @property
    def object(self):
        return self._object

    def set_name(self, name):
        self._name = name

    def set_district(self, district_name):
        self._district = Entities().get_district(district_name)

    def set_id(self, id):
        self._id = id

    def set_object(self, object):
        self._object = object

    def from_object(self, object):
        '''Rewrite all data in self class User by database from Users object'''
        self._name =  object.name
        self._id = object.id
        self._district = Entities().get_district(object) # todo how get district by name
        self._object = object