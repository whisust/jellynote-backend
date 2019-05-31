from . import Notifications, new_transaction, RangeQuery, PaginatedQuery

from typing import List

from psycopg2.extras import execute_values

from models.jellynote import Song, Notification
from . import Notifications, new_transaction, RangeQuery, PaginatedQuery

_list_query_date_range = "SELECT " + Notifications.all_fields() + \
                         " FROM " + Notifications.name + \
                         " WHERE user_id = %s AND created_at BETWEEN %s AND %s ORDER BY created_at DESC"


def _list_query_pagination(req: PaginatedQuery):
    return "SELECT " + Notifications.all_fields() + \
           " FROM " + Notifications.name + \
           " WHERE user_id = %s ORDER BY created_at DESC LIMIT " + str(req.count) + " OFFSET " + str(req.offset)


_insert_query = "INSERT INTO " + Notifications.name + " (song_id, user_id, message) VALUES %s"

_count_query = "SELECT COUNT(*) FROM " + Notifications.name + " WHERE user_id = %s"


def list_all(user_id, req) -> List[Song]:
    with new_transaction() as cur:
        if isinstance(req, RangeQuery):
            cur.execute(_list_query_date_range, (user_id, req.furthest, req.closest))
        else:
            cur.execute(_list_query_pagination(req), (user_id,))
        return [Notification.from_row(row) for row in cur.fetchall()]


def insert(notification_creation_values):
    with new_transaction() as cur:
        execute_values(cur, _insert_query, notification_creation_values)


def count(user_id):
    with new_transaction() as cur:
        cur.execute(_count_query, (user_id,))
        return cur.fetchone()[0]
