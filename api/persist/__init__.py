from dataclasses import dataclass
from datetime import datetime
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

Notifications = Table('notifications',
                      'n',
                      ['id', 'song_id', 'user_id', 'message', 'created_at'])

tables = [Users, Songs, Notifications]


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


@dataclass(frozen=True)
class RangeQuery:
    """Holds lower and upper bound for a range query"""
    furthest: datetime
    closest: datetime

    @staticmethod
    def from_query_string(query_string):
        d1, d2 = [datetime.fromisoformat(x) for x in query_string.split('_')]
        return RangeQuery(furthest=min(d1, d2), closest=max(d1, d2))


@dataclass(frozen=True)
class PaginatedQuery:
    """Holds offset and limit values for a paginated query"""
    offset: int
    count: int

    @staticmethod
    def from_query_string(query_string):
        low, up = [int(x) for x in query_string.split('_')]
        offset = low
        count = up - low
        return PaginatedQuery(offset, count)
