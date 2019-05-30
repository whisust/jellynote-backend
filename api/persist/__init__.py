from dataclasses import dataclass
from typing import List
from models.errors import BaseError
import psycopg2
from contextlib import contextmanager

connection_info = {
    'database': "jellynote",
    'user': "jelly",
    'password': "j3llynote",
    'host': "localhost",
    'port': "5432"
}

conn = psycopg2.connect(**connection_info)


@contextmanager
def new_transaction():
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    except psycopg2.Error as e:
        raise PersistError("An unexpected database exception occured", e)


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


@dataclass
class InsertionError(BaseError):
    message: str


@dataclass
class PersistError(BaseError):
    message: str
    exception: Exception


@dataclass
class UpdateError(BaseError):
    message: str


def is_unique_constraint_violation(err):
    return err.pgcode == '23505'
