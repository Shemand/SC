import json
import os

from backend.src.sc_config.repositories_models import DatabaseRepositoryConfig, PuppetRepositoryConfig, \
    DallasRepositoryConfig, KasperskyRepositoryConfig, ADRepositoryConfig


class JsonConfigurationStorage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        with open(self.file_path, 'r') as file:
            return json.loads(file.read())

    def write_data(self, data):
        with open(self.file_path, 'w') as file:
            return file.write(json.dumps(data))


class Configuration: # todo validation unit services and end the services list
    def __init__(self):
        path = os.getcwd()
        path = os.path.join(path, 'configs')
        path = os.path.join(path, 'new_configs')
        units_path = os.path.join(path, 'units.json')
        structure_path = os.path.join(path, 'structure.json')
        repositories_path = os.path.join(path, 'repositories.json')
        system_path = os.path.join(path, 'system.json')
        unit_repository_settings_path = os.path.join(path, 'unit_repository_settings.json')
        unit_repositories_path = os.path.join(path, 'unit_repositories.json')

        self.units = UnitsConfiguration(units_path, structure_path, unit_repositories_path,
                                        unit_repository_settings_path)

        self.repositories = RepositoriesConfiguration(repositories_path)

        self._system = JsonConfigurationStorage(system_path)


class UnitsConfiguration:
    def __init__(self, units_path: str, structure_path: str,
                 unit_repositories_path: str, unit_repository_settings: str):

        self.units_storage = JsonConfigurationStorage(units_path)
        self.structure_storage = JsonConfigurationStorage(structure_path)
        self.repositories_storage = JsonConfigurationStorage(unit_repositories_path)
        self.repository_settings_storage = JsonConfigurationStorage(unit_repository_settings)

        self.main = self.units_storage.data
        self.structure = self.structure_storage.data
        self.repositories = self.repositories_storage.data
        self.repository_settings = self.repository_settings_storage.data

        self._validate_units()
        self._validate_structure()
        self._validate_repositories()
        self._validate_repository_settings()

        self.unit_names = [unit_name for unit_name in self.main]

    def _validate_structure(self):
        structure = self.structure
        for parent, child in structure.items():
            if not parent in self.main:
                raise UnitStructureException(f"Unknown parent name ({parent}) in structure.json")
            if child and not child in self.main:
                raise UnitStructureException(f"Unknown children name ({child}) in structure.json")

    def _validate_units(self):
        units = self.main
        default = None
        for unit_name, caption in units.items():

            if unit_name == 'DEFAULT' and caption is None:
                raise UnitNameException(f'DEFAULT section can\'t be a null')
            elif unit_name == 'DEFAULT' and default is not None:
                raise UnitNameException('DEFAULT section has duplicated')
            else:
                default = unit_name

            if caption is None:
                UnitNameException(f"Unit with name ({unit_name}) must have caption string")
            if not isinstance(caption, str):
                UnitNameException(f'Unit with name ({unit_name}) don\'t have parameter of string. Please edit configuration file.')
        if not default:
            UnitNameException('Units config must have "DEFAULT" section with any value')

    def _validate_repositories(self):
        repositories = self.repositories
        for unit_name in self.main:
            if unit_name == 'DEFAULT':
                continue
            if not unit_name in repositories:
                raise UnitRepositoriesException(f"Unit with name '{unit_name}' haven't record in unit repositories config")
            if not isinstance(repositories[unit_name], list):
                raise UnitRepositoriesException(f"Record with name ({unit_name}) of unit repositories not a list")

    def _validate_repository_settings(self):
        repository_settings = self.repository_settings
        for unit_name in self.main:
            if unit_name == 'DEFAULT':
                continue
            if not unit_name in repository_settings:
                raise UnitRepositorySettingsException(f"Unit with name '{unit_name}' haven't record in repository settings config")
            if not isinstance(repository_settings[unit_name], dict):
                raise UnitRepositorySettingsException(f"Record with name ({unit_name}) of repository settings not a list")
            if not 'dallas_containers' in repository_settings[unit_name]\
                    or not isinstance(repository_settings[unit_name]['dallas_containers'], list):
                raise UnitRepositorySettingsException(f"Record with name ({unit_name}) hasn't 'dallas_container'")
            if not 'active_directory_containers' in repository_settings[unit_name] \
                    or not isinstance(repository_settings[unit_name]['active_directory_containers'], list):
                raise UnitRepositorySettingsException(f"Record with name ({unit_name}) hasn't 'active_directory_containers'")


class RepositoriesConfiguration:
    def __init__(self, repositories_path):
        config = JsonConfigurationStorage(repositories_path)
        self.active, self.inactive = self._transform_to_models(config)

    def _transform_to_models(self, repositories):
        active = {
            "kaspersky": [],
            "dallas": [],
            "puppet": [],
            "database": [],
            "active_directory": []
        }
        inactive = {**active}
        for repo in repositories.data:
            r_type = repo['type']
            actived = repo['active']
            if r_type == 'active_directory':
                if actived: active['active_directory'].append(ADRepositoryConfig(**repo))
                else: inactive['active_directory'].append(ADRepositoryConfig(**repo))
            elif r_type == 'kaspersky':
                if actived: active['kaspersky'].append(KasperskyRepositoryConfig(**repo))
                else: inactive['kaspersky'].append(KasperskyRepositoryConfig(**repo))
            elif r_type == 'dallas':
                if actived: active['dallas'].append(DallasRepositoryConfig(**repo))
                else: inactive['dallas'].append(DallasRepositoryConfig(**repo))
            elif r_type == 'puppet':
                if actived: active['puppet'].append(PuppetRepositoryConfig(**repo))
                else: inactive['puppet'].append(PuppetRepositoryConfig(**repo))
            elif r_type == 'database':
                if actived: active['database'].append(DatabaseRepositoryConfig(**repo))
                else: inactive['database'].append(DatabaseRepositoryConfig(**repo))
            else:
                raise RepositoriesTransformException(f"Repository with name {repo['connection_name']} has unknown type.")
        return active, inactive
# ----- EXCEPTIONS --------

class UnitConfigException(Exception):
    pass


class UnitStructureException(UnitConfigException):
    pass


class UnitNameException(UnitConfigException):
    pass


class UnitRepositoriesException(UnitConfigException):
    pass


class UnitRepositorySettingsException(UnitConfigException):
    pass


class RepositoriesConfigException(Exception):
    pass


class RepositoriesTransformException(RepositoriesConfigException):
    pass