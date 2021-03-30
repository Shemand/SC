from backend.sc_database.updaters.DatabaseUpdaterAbstract import DatabaseUpdaterAbstract


class ComputersUpdater(DatabaseUpdaterAbstract):

    def __init__(self, database):
        self.cached_computers_id = {}
        self.cached_computers_name = {}
        self._database = database
        self._session = database.session
        self._mdl_computers = type(database).Computers
        self._mdl_active_directory = type(database).Computers_ActiveDirectory

    def add_computer(self, computer_name):
        computer_obj = self.get_computer_object(computer_name)
        if computer_obj:
            return False
        new_computer = self._mdl_computers(name=computer_name)
        self._session.add(new_computer)
        self.get_computer_object(computer_name)
        self.commit()
        return True

    def remove_computer(self, computer):
        computer_obj = self.get_computer_object(computer)
        if computer_obj is not None:
            self._session.delete(computer_obj)
            self.__delete_from_cache(computer_obj)
            self.commit()
            return True
        return False

    def change_name(self, computer, new_name):
        computer_obj = self.get_computer_object(computer)
        if not self._database.query(self._mdl_computers).filter_by(name=new_name).first():
            computer_obj.name = new_name
            return True
        return False

    def change_comment(self, computer, comment):
        computer_obj = self.get_computer_object(computer)
        computer_obj.comment = comment
        return True

    def commit(self):
        self._session.commit()
        return True

    def register_active_directory(self, computer_name, information_dict):
        if not isinstance(information_dict, dict):
            raise (RuntimeError("argument information_dict in register_active_directory is not Dict class"))
        if not 'unit_name' in information_dict or not 'unit_id' in information_dict:
            raise (RuntimeError("argument information_dict of register_active_directory hasn't 'unit_name' or 'unit_id'"))
        computer_obj = self.get_computer_object()
        if computer_obj:
            ad = computer_obj.active_directory
            if ad:
                return ad, False  # (obj, boolean created or not)
            computer_obj.active_directory = self._mdl_active_directory(**information_dict)
            return ad, True
        return None, False

    def delete_active_directory(self, computer_name):
        computer_obj = self.get_computer_object(computer_name)

    def get_computer_object(self, computer):
        _, type = self.__get_computer_argument_type(computer)
        computer_obj = self.__get_from_cache(computer, type)
        if not computer_obj:
            base_query = self._database.query(self._mdl_computers)
            if type == 'id':
                computer_obj = base_query.filter_by(id=computer).first()
            elif type == 'name':
                computer_obj = base_query.filter_by(name=computer).first()
            else:
                return None
            if computer_obj is not None:
                self.cached_computers_id[computer_obj.id] = computer_obj
                self.cached_computers_name[computer_obj.name] = computer_obj
        return computer_obj

    def __get_computer_argument_type(self, computer):
        if isinstance(computer, int):
            return computer, 'id'
        if isinstance(computer, str):
            return computer, 'name'
        if isinstance(computer, self._mdl_computers):
            return computer, 'object'
        raise RuntimeError('Unknown type of computer in ComputersUpdater.__get_computer_object')

    def __get_from_cache(self, computer, type):
        if type == 'id':
            if computer in self.cached_computers_id:
                return self.cached_computers_id[computer]
            return None
        if type == 'name':
            if computer in self.cached_computers_name:
                return self.cached_computers_name[computer]
            return None
        if type == 'object':
            return computer
        raise RuntimeError('Unknown type of computer cache')

    def __clear_cache(self):
        self.cached_computers_name = {}
        self.cached_computers_id = {}

    def __delete_from_cache(self, computer_object):
        if computer_object.name in self.cached_computers_name:
            del self.cached_computers_name[computer_object.name]
        if computer_object.id in self.cached_computers_id:
            del self.cached_computers_id[computer_object.id]

    def computer_has_ad(self, computer_name):
        computer_obj = self.__get_computer_object(computer_name)
        if computer_obj.active_directory:
            return True
        return False

    def load_all_computers_in_cache(self):
        computers_objects = self._session.query(self._mdl_computers).all()
        for computer_obj in computers_objects:
           self.cached_computers_id[computer_obj.id] = computer_obj
           self.cached_computers_name[computer_obj.name] = computer_obj
