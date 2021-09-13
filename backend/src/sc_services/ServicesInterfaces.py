from backend.src.sc_repositories.DatabaseRepository import DatabaseRepository


class DatabaseServiceInterface:
    def __init__(self, database: DatabaseRepository):
        ...