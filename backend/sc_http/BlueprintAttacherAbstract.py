from flask import Blueprint


class BlueprintAttacherAbstract:
    def __init__(self,mod: Blueprint, base_name:str) -> None:
        self.base_path = '/' + base_name + '/'
        self.mod = mod
        self.attach_to_blueprint(self.mod)
        print('all right')

    def to_path(self, path: str) -> str:
        if path == '/':
            return self.base_path
        return self.base_path + path

    def attach_to_blueprint(self, mod: Blueprint) -> None:
        assert False, 'Method must be released!'