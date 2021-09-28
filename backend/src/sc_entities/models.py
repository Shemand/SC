from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy.cresultproxy import BaseRow


class UnitBase(BaseModel):
    id_: Optional[int]
    name: str = Field()


class Unit(UnitBase):
    children: list
    repositories: list


class CryptoGateway(BaseModel):
    name: str
    caption: str
    address: str
    mask: int


class Os(BaseModel):
    id_: Optional[int]
    name: str
    isUnix: bool


class Ip(BaseModel):
    id_: Optional[int]
    ipv4: str
    isAllowed: Optional[datetime]


class ADUser(BaseModel):
    name: str
    full_name: Optional[str]
    department: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    registred: Optional[datetime]
    last_logon: Optional[datetime]
    isDeleted: Optional[datetime]
    isDisabled: Optional[datetime]
    isLocked: Optional[datetime]


class UserBase(BaseModel):
    login: str
    privileges: int
    unit: Unit


class User(UserBase):
    ad: Optional[ADUser]


class ComputerBase(BaseModel):
    id_: Optional[int]
    name: str
    unit: UnitBase


class Computer(ComputerBase):
    comment: Optional[str]


class Dallas(BaseModel):
    computer: ComputerBase
    status: int
    server: str
    isDeleted: Optional[datetime]


class Puppet(BaseModel):
    computer: ComputerBase
    ip: Optional[Ip]
    os: Optional[Os]
    board_serial: str
    astra_update: str
    environment: str
    domain: str
    serial_number: str
    isVirtual: bool
    mac: str
    kesl: str
    kl_agent: str
    update_seconds: int
    isDeleted: Optional[int]


class Kaspersky(BaseModel):
    computer: ComputerBase
    os: Optional[Os]
    ip: Optional[Ip]
    agent: str
    security: str
    server: str
    isDeleted: Optional[datetime]


class ADComputer(BaseModel):
    computer: ComputerBase
    isDeleted: Optional[datetime]
    last_visible: Optional[datetime]
    isActive: bool
    registred: Optional[datetime]
