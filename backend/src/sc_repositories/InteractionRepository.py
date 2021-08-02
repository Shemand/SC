from typing import Any

from backend.src.sc_repositories.BaseRepository import BaseRepository


class InteractionRepository(BaseRepository):

    DISABLED = 'disabled'
    INACTIVE = 'inactive'
    INWORK = 'inwork'
    ACTIVE = 'active'
    STATUSES = [DISABLED, INACTIVE, INWORK, ACTIVE]

    _name: str = ''
    _connection: Any
    _configuration: dict

    def __init__(self, district, main_config, specific_data):
        self._district = district
        self._name = main_config['connection_name']
        self._ip = main_config['connection_ip']
        self._port = main_config['connection_port']
        self._configuration = specific_data
        self._connection = None
        self._status = 'inactive'

    @property
    def configuration(self):
        return self._configuration

    @property
    def name(self):
        return self._name

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def district(self):
        return self._district

    @property
    def status(self):
        return self._status

    def create_connection(self) -> Any:
        assert False, 'Method must be released!'

    @property
    def connection(self) -> Any:
        if self._connection is not None:
            return self._connection
        self._connection = self.create_connection()
        if self._connection is None:
            raise BaseException('Connection with (' + self.name + ') was failed.')
        self.check_connection()

    def check_connection(self) -> bool:
        assert False, 'Method must be released!'
