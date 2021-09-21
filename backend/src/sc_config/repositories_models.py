from pydantic import BaseModel


class SpecDataRepositoryConfig(BaseModel):
    ...


class RepositoryConfig(BaseModel):
    name: str
    ip: str
    port: str
    type: str
    active: bool
    specific_data: SpecDataRepositoryConfig


class SpecADConfig(SpecDataRepositoryConfig):
    username: str
    password: str
    path: str
    begin_node: str
    end_nodes: list


class SpecPuppetConfig(SpecDataRepositoryConfig):
    fields: list
    prefixes: list


class SpecKasperskyConfig(SpecDataRepositoryConfig):
    username: str
    password: str
    server: str


class SpecDallasConfig(SpecDataRepositoryConfig):
    server: str


class SpecDatabaseConfig(SpecDataRepositoryConfig):
    database: str
    driver: str
    username: str
    password: str


class ADRepositoryConfig(RepositoryConfig):
    specific_data: SpecADConfig


class PuppetRepositoryConfig(RepositoryConfig):
    specific_data: SpecPuppetConfig


class KasperskyRepositoryConfig(RepositoryConfig):
    specific_data: SpecKasperskyConfig


class DallasRepositoryConfig(RepositoryConfig):
    specific_data: SpecDallasConfig


class DatabaseRepositoryConfig(RepositoryConfig):
    specific_data: SpecDatabaseConfig
