from backend.sc_config.config import config


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
        assert district_name in self.__districts, f'Unknown district_name ({district_name} in Entities.get_district)'
        return self.__districts[district_name]