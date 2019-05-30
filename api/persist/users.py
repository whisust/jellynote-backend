from . import conn, Users, InsertionError, new_transaction

from models.jellynote import User
from models.requests import UserCreationRequest

import psycopg2

from serde import encode_enum_iterable


def _list_query(limit: int):
    return "SELECT " + Users.all_fields() + " FROM " + Users.name + " LIMIT " + str(limit)


_insert_query = "INSERT INTO " + Users.name + " (name, email, instruments) VALUES (%s, %s, %s) RETURNING " + Users.all_fields()


def list_all(limit: int):
    with conn.cursor() as cur:
        cur.execute(_list_query(limit))
        return [User.from_row(row) for row in cur.fetchall()]


def insert(req: UserCreationRequest) -> User:
    with new_transaction() as cursor:
        try:
            cursor.execute(_insert_query, (req.name, req.email, encode_enum_iterable(req.instruments)))
            return User.from_row(cursor.fetchone())
        except psycopg2.Error as e:
            raise InsertionError("A user with email=" + req.email + " already exists")
