from backend.sc_database.model.Computers import Computers
from .DatabaseActionsAbstract import DatabaseActionsAbstract


class ComputerActions(DatabaseActionsAbstract):

    def __init__(self, database, model):
        super().__init__(database, model)


