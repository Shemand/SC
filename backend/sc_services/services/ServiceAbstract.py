from typing import Any


class ServiceAbstract:

    _name: str = ''
    _connection: Any
    _configuration: dict

    def __init__(self, connection_name: str, configuration: dict):
        self._name = connection_name
        self._configuration = configuration
        self._connection = None

    def create_connection(self) -> Any:
        assert False, 'Method must be released!'

    def check_connection(self) -> bool:
        assert False, 'Method must be released!'

    @property
    def connection(self) -> Any:
        if self._connection is not None:
            return self._connection
        self._connection = self.create_connection()
        if self._connection is None:
            raise BaseException('Connection with (' + self.name + ') was failed.')
        self.check_connection()

    @property
    def configuration(self):
        return self._configuration

    @property
    def name(self):
        return self._name
