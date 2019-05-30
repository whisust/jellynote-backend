from . import conn, Songs, InsertionError, new_transaction, UpdateError, is_unique_constraint_violation

from models.jellynote import Song, SongId
from models.requests import SongCreationRequest, SongUpdateRequest

import psycopg2

from typing import Optional, List

from serde import encode_enum_iterable

_returning_clause = " RETURNING " + Songs.all_fields()


def _list_query(limit: int):
    return "SELECT " + Songs.all_fields() + " FROM " + Songs.name + " ORDER BY updated_at DESC LIMIT " + str(limit)


_insert_query = "INSERT INTO " + Songs.name + " (title, instruments) VALUES (%s, %s)" + _returning_clause

_find_one_query = "SELECT " + Songs.all_fields() + " FROM " + Songs.name + " WHERE id=%s"

_update_query = "UPDATE " + Songs.name + " SET title = %s, updated_at = now() WHERE id = %s" + _returning_clause

_delete_query = "DELETE FROM " + Songs.name + " WHERE id = %s"


def list_all(limit: int) -> List[Song]:
    with new_transaction() as cur:
        cur.execute(_list_query(limit))
        return [Song.from_row(row) for row in cur.fetchall()]


def insert(req: SongCreationRequest) -> Song:
    with new_transaction() as cur:
        cur.execute(_insert_query, (req.title, encode_enum_iterable(req.instruments)))
        return Song.from_row(cur.fetchone())


def find(song_id: SongId) -> Optional[Song]:
    with new_transaction() as cur:
        cur.execute(_find_one_query, (song_id,))
        row = cur.fetchone()
        if row is not None:
            return Song.from_row(row)
        else:
            return None


def update(song_id: SongId, req: SongUpdateRequest) -> Song:
    with new_transaction() as cur:
        cur.execute(_update_query, (req.title, song_id))
        return Song.from_row(cur.fetchone())


def delete(song_id: SongId):
    with new_transaction() as cur:
        cur.execute(_delete_query, (song_id,))
