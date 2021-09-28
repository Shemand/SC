import json
import os
from typing import Optional

from backend.src.sc_config.repositories_models import DatabaseRepositoryConfig, PuppetRepositoryConfig, \
    DallasRepositoryConfig, KasperskyRepositoryConfig, ADRepositoryConfig, RepositoryConfig
from backend.src.sc_entities.models import Unit


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


class Configuration:  # todo validation unit services and end the services list
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
            cls.instance.load()
        return cls.instance

    def load(self):
        self.types = {  # todo load types from any config file
            "active_directory": ADRepositoryConfig,
            "dallas": DallasRepositoryConfig,
            "puppet": PuppetRepositoryConfig,
            "database": DatabaseRepositoryConfig,
            "kaspersky": KasperskyRepositoryConfig
        }
        path = os.getcwd()
        path = os.path.join(path, 'configs')
        path = os.path.join(path, 'new_configs')
        units_path = os.path.join(path, 'units.json')
        structure_path = os.path.join(path, 'structure.json')
        repositories_path = os.path.join(path, 'repositories.json')
        system_path = os.path.join(path, 'system.json')
        unit_repository_settings_path = os.path.join(path, 'unit_repository_settings.json')
        unit_repositories_path = os.path.join(path, 'unit_repositories.json')

        self._units = UnitsConfiguration(units_path, structure_path, unit_repositories_path,
                                         unit_repository_settings_path)

        self._repositories = RepositoriesConfiguration(repositories_path, self.types)

        self._system = JsonConfigurationStorage(system_path)
        self._validate_services_names()

    def _validate_services_names(self):
        repositories = self._repositories.names
        for unit_name, repos in self._units.repositories.items():
            for repo in repos:
                if not repo in repositories:
                    raise Exception(f'Unit ({unit_name}) have unknown repository - ({repo}). Check the file')

    @property
    def database(self) -> DatabaseRepositoryConfig:
        return self._repositories.active_db

    @property
    def repositories(self) -> dict:
        return self._repositories.all

    def unit(self, unit_name) -> Unit:
        return self._units.get(unit_name)

    def repository(self, repository_name) -> RepositoryConfig:
        return self._repositories.get(repository_name)

    def get_active_repos(self, repos_type) -> []:
        return {repo_name: repo
                for repo_name, repo in self._repositories.all.items()
                if repo.type == repos_type and repo.active is True
                }


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

        self.cache = self.Cache()

    class Cache:
        def __init__(self):
            self.units = {}

        def get(self, unit_name):
            if not unit_name in self.units:
                return None
            return self.units[unit_name]

        def set(self, unit_name, model):
            self.units[unit_name] = model

    def get(self, unit_name) -> (Optional[Unit], list):
        if not unit_name in self.unit_names:
            raise TypeError(f"You attempted get not exists unit (unit name: {unit_name}")

        cached = self.cache.get(unit_name)
        if cached:
            return cached

        repositories = []
        repositories.extend(self.repositories[unit_name])
        children = []
        for child, parent in self.structure.items():
            if parent == unit_name:
                unit, repos = self.get(child)
                repositories.extend(repos)
                children.append(unit)

        unit = Unit(name=unit_name, children=children, repositories=repositories)
        self.cache.set(unit_name, unit)
        return unit, repositories

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
                UnitNameException(
                    f'Unit with name ({unit_name}) don\'t have parameter of string. Please edit configuration file.')
        if not default:
            UnitNameException('Units config must have "DEFAULT" section with any value')

    def _validate_repositories(self):
        repositories = self.repositories
        for unit_name in self.main:
            if unit_name == 'DEFAULT':
                continue
            if not unit_name in repositories:
                raise UnitRepositoriesException(
                    f"Unit with name '{unit_name}' haven't record in unit repositories config")
            if not isinstance(repositories[unit_name], list):
                raise UnitRepositoriesException(f"Record with name ({unit_name}) of unit repositories not a list")

    def _validate_repository_settings(self):
        repository_settings = self.repository_settings
        for unit_name in self.main:
            if unit_name == 'DEFAULT':
                continue
            if not unit_name in repository_settings:
                raise UnitRepositorySettingsException(
                    f"Unit with name '{unit_name}' haven't record in repository settings config")
            if not isinstance(repository_settings[unit_name], dict):
                raise UnitRepositorySettingsException(
                    f"Record with name ({unit_name}) of repository settings not a list")
            if not 'dallas_containers' in repository_settings[unit_name] \
                    or not isinstance(repository_settings[unit_name]['dallas_containers'], list):
                raise UnitRepositorySettingsException(f"Record with name ({unit_name}) hasn't 'dallas_container'")
            if not 'active_directory_containers' in repository_settings[unit_name] \
                    or not isinstance(repository_settings[unit_name]['active_directory_containers'], list):
                raise UnitRepositorySettingsException(
                    f"Record with name ({unit_name}) hasn't 'active_directory_containers'")


class RepositoriesConfiguration:
    def __init__(self, repositories_path, types):
        config = JsonConfigurationStorage(repositories_path)

        self.types = types
        self._repositories = self._transform_to_models(config)
        self._validate_duplicates()
        self._validate_database()

    @property
    def all(self):
        repos = {}
        for t in self.types:
            for repo_name, repo in self._repositories[t].items():
                repos[repo_name] = repo
        return repos

    @property
    def active_db(self):
        active_databases = [repo for _, repo in self.database.items() if repo.active is True]
        if len(active_databases) > 1 or len(active_databases) == 0:
            raise RepositoriesConfigException("can't get active database because it's not equal 1")
        return active_databases[0]

    @property
    def active(self):
        return {repo_name: repo for repo_name, repo in self.all.items() if repo.active is True}

    @property
    def inactive(self):
        return {repo_name: repo for repo_name, repo in self.all.items() if repo.active is False}

    @property
    def names(self):
        return [repo_name for repo_name in self.all]

    def __getattr__(self, key):
        if not key in self.types:
            raise AttributeError(f'RepositoryConfiguration haven\'t attribute {key}')
        return self._repositories[key]

    def __getitem__(self, key):
        for t in self.types:
            if key in self._repositories[t]:
                return self._repositories[t][key]
        raise KeyError(f"RepositoryConfiguration haven't repository ({key})")

    def get(self, repository_name):
        if not repository_name in self.repository_names:
            return None
        return self.repository_names

    def _validate_duplicates(self):
        names = []
        for repo_name in self.all:
            if repo_name in names:
                raise RepositoriesConfigException("repo.name duplicated in config file.")
            names.append(repo_name)

    def _validate_database(self):
        databases = [db_name for db_name, db in self.database.items() if db.active == True]
        if len(databases) > 1:
            raise RepositoryTypeException("Config have more then 1 active database repository.")
        if len(databases) == 0:
            raise RepositoryTypeException("Repository Config must have 1 active database.")

    def _transform_to_models(self, repositories):  # todo automate choice the type
        repositories_storage = {
        }
        for t in self.types:
            repositories_storage[t] = {}
        for repo in repositories.data:
            r_type = repo['type']
            repositories_storage[r_type][repo['name']] = self._get_repo_type(r_type)(**repo)
            if not r_type in self.types:
                raise RepositoriesTransformException(
                    f"Repository with name {repo['name']} has unknown type.")
        return repositories_storage

    def _get_repo_type(self, repository_type):
        if not repository_type in self.types:
            raise RepositoryTypeException("Repositories config have some wrong type.")
        return self.types[repository_type]


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


class RepositoryTypeException(RepositoriesConfigException):
    pass
