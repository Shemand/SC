from sqlalchemy.orm import Session

from backend.sc_services.ServiceAbstract import ServiceAbstract


class DatabaseService(ServiceAbstract):

    def __init__(self, configurations: dict) -> None:
        super().__init__(configurations['connection_name'])


    def create_connection(self):
        self._connection = Session()
        return self._connection

    def check_connection(self) -> bool:
        if self._session == None:
            return False
        return True

    def commit(self):
        self.connection.commit()