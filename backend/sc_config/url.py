import json
import os

FILE_NAMES = ["api.json"]


class ModuleRequest:

    AUTH = 'auth'
    UNAUTH = 'unauthed'
    ANY = 'ANY'
    ADMIN = 'admin'
    REQUIRES = [AUTH, UNAUTH, ANY, ADMIN]

    def __init__(self, name=None, description=None,
                 isAuth=ANY, data={}):
        self.name = name
        self.description = description
        self.isAuth = isAuth
        self.data = data

class ModuleUrls:

    def __init__(self, module_name, module_information):
        self.name = module_name
        self.get = self._init_module_request(module_information['GET'])
        self.post = self._init_module_request(module_information['POST'])
        self.put = self._init_module_request(module_information['PUT'])
        self.delete = self._init_module_request(module_information['DELETE'])
        children = module_information['children']
        self.sub_modules = { name : ModuleUrls(name, children[name]) for name in children}

    def _init_module_request(self, module_information):
        if module_information == {}:
            return None
        assert 'name' in module_information, f'{self.name} haven\'t name in specification of some method'
        assert 'description' in module_information, f'{self.name} haven\'t description in specification of some method'
        assert 'isAuth' in module_information, f'{self.name} haven\'t isAuth in specification of some method'
        kwargs = {
            "name" : module_information['name'],
            "description" : module_information['description'],
            "isAuth" : module_information['isAuth']
        }
        if module_information['data'] == {}:
            kwargs['data'] = module_information['data']
        return ModuleRequest(**kwargs)


class UrlPaths:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UrlPaths, cls).__new__(cls)
            cls.__initialized = False
        return cls.instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.modules_names = []
            self.modules = {}
            for file_name in FILE_NAMES:
                module_name = file_name.split('.')[0]
                self.modules_names.append(module_name)
                json_dict = self.__json_file_to_dict(self.__get_file_path(file_name))
                self.description = json_dict['description']
                for name in json_dict['urls']:
                    self.modules[name] = ModuleUrls(module_name, json_dict['urls'][name])


    def __get_file_path(self, file_name):
        abs_path = os.getcwd()
        file_path = os.path.join(abs_path, 'sc_config')
        file_path = os.path.join(file_path, file_name)
        return file_path

    def __json_file_to_dict(self, file_path):
        file = open(file_path, 'r')
        json_dict = json.loads(file.read())
        file.close()
        return json_dict
