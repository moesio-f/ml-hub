"""Esse módulo contém definição das
entidades manipuladas pelo sistema.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, fields

from datetime import datetime


@dataclass
class UserJWT:
    username: str
    user_type: str
    creation_date: str  # %d/%m/%y-%H:%M:%S
    expiration_date: str  # %d/%m/%y-%H:%M:%S
    jwt: str
    key: str

    def asdict(self):
        return asdict(self)

    def is_expired(self) -> bool:
        expiration = datetime.strptime(
            self.expiration_date, "%d/%m/%y-%H:%M:%S")
        return expiration < datetime.now()
    
    @staticmethod
    def loadFromDict(v) -> UserJWT:
        fieldSet = {f.name for f in fields(UserJWT) if f.init}
        filteredArgDict = {k : v for k, v in v.items() if k in fieldSet}
        return UserJWT(**filteredArgDict)


@dataclass
class User:
    username: str
    password: str
    user_type: str
    permissions: list[str]
