from .DatabaseActionsAbstract import DatabaseActionsAbstract


class AddressActions(DatabaseActionsAbstract):

    def __init__(self, database, model):
        super().__init__(database, model)

