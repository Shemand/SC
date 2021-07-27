from ..sc_config.config import config


class Entities:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Entities, cls).__new__(cls)
            cls.__created = True
        return cls.instance

    def __init__(self):
        if Entities.__created is True:
            Entities.__created = False
            self.__config = config
            self.__districts = self.__config.districts

    def get_district(self, district_name):
        district_name = district_name.upper()
        assert district_name in self.__districts, f'Unknown district_name ({district_name} in Entities.get_district)'
        return self.__districts[district_name]

    def get_user(self, district_name, user_id=None, user_name=None):
        if not district_name in self.__districts:
            raise RuntimeError(f'Entities.get_user haven\'t district with name - "{district_name}"')
        district = self.get_district(district_name)
        if isinstance(user_id, int):
            district.database.Users
        elif isinstance(user_name, str):
            pass
        else:
            raise ValueError('Entities.get_user params must have argument user_id or user_name')