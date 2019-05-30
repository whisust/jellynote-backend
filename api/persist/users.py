from . import conn, Users, InsertionError, new_transaction, UpdateError, is_unique_constraint_violation

from models.jellynote import User, UserId
from models.requests import UserCreationRequest, UserUpdateRequest

import psycopg2

from typing import Optional, List

from serde import encode_enum_iterable

_returning_clause = " RETURNING " + Users.all_fields()


def _list_query(limit: int):
    return "SELECT " + Users.all_fields() + " FROM " + Users.name + " ORDER BY updated_at DESC LIMIT " + str(limit)


_insert_query = "INSERT INTO " + Users.name + " (name, email, instruments) VALUES (%s, %s, %s)" + _returning_clause

_find_one_query = "SELECT " + Users.all_fields() + " FROM " + Users.name + " WHERE id=%s"


def list_all(limit: int) -> List[User]:
    with new_transaction() as cur:
        cur.execute(_list_query(limit))
        return [User.from_row(row) for row in cur.fetchall()]


def insert(req: UserCreationRequest) -> User:
    with new_transaction() as cur:
        try:
            cur.execute(_insert_query, (req.name, req.email, encode_enum_iterable(req.instruments)))
            return User.from_row(cur.fetchone())
        except psycopg2.Error as e:
            if is_unique_constraint_violation(e):
                raise InsertionError("A user with email=" + req.email + " already exists")
            else:
                raise


def find(user_id: UserId) -> Optional[User]:
    with new_transaction() as cur:
        cur.execute(_find_one_query, (user_id,))
        row = cur.fetchone()
        if row is not None:
            return User.from_row(row)
        else:
            return None
