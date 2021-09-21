from pydantic import BaseModel


class SpecDataServiceConfig(BaseModel):
    ...


class ServiceConfig(BaseModel):
    name: str
    ip: str
    port: str
    type: str
    active: bool
    specific_data: SpecDataServiceConfig


class SpecADConfig(SpecDataServiceConfig):
    username: str
    password: str
    path: str
    begin_node: str
    end_nodes: [str]


class SpecPuppetConfig(SpecDataServiceConfig):
    fields: [str]
    prefixes: [str]


class SpecKasperskyConfig(SpecDataServiceConfig):
    username: str
    password: str
    server: str


class SpecDallasConfig(SpecDataServiceConfig):
    server: str


class SpecDatabaseConfig(SpecDataServiceConfig):
    database: str
    driver: str
    username: str
    password: str


class ADServiceConfig(ServiceConfig):
    specific_data: SpecADConfig


class PuppetServiceConfig(ServiceConfig):
    specific_data: SpecPuppetConfig


class KasperskyServiceConfig(ServiceConfig):
    specific_data: SpecKasperskyConfig


class DallasServiceConfig(ServiceConfig):
    specific_data: SpecDallasConfig


class DatabaseServiceConfig(ServiceConfig):
    specific_data: SpecDatabaseConfig
