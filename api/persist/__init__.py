from dataclasses import dataclass
from typing import List
from models.errors import BaseError
import psycopg2

connection_info = {
    'database': "jellynote",
    'user': "jelly",
    'password': "j3llynote",
    'host': "localhost",
    'port': "5432"
}

conn = psycopg2.connect(**connection_info)


@dataclass(frozen=True)
class Table(object):
    name: str
    alias: str
    fields: List[str]

    def all_fields(self):
        return ', '.join(self.fields)

    def all_fields_aliased(self):
        return ', '.join(map(lambda x: alias + '.' + x, self.fields))


Users = Table('users',
              'u',
              ['id', 'name', 'email', 'instruments', 'created_at', 'updated_at'])

tables = [Users]


@dataclass(frozen=True)
class InsertionError(BaseError):
    message: str


@dataclass(frozen=True)
class PersistError(BaseError):
    message: str
    exception: Exception


@dataclass(frozen=True)
class UpdateError(BaseError):
    message: str
