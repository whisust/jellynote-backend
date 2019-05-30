from dataclasses import dataclass
from typing import List
from models.errors import BaseError
import psycopg2
from contextlib import contextmanager
from config import conf

connection_info = {
    'database': conf.db.database,
    'user': conf.db.user,
    'password': conf.db.password,
    'host': conf.db.host,
    'port': conf.db.port
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
        return ', '.join(map(lambda x: self.alias + '.' + x, self.fields))


Users = Table('users',
              'u',
              ['id', 'name', 'email', 'instruments', 'created_at', 'updated_at'])

Songs = Table('songs',
              's',
              ['id', 'title', 'instruments', 'created_at', 'updated_at'])

tables = [Users, Songs]


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
