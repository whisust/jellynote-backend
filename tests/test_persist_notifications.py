import pytest
from datetime import datetime
from persist import notifications, PaginatedQuery, RangeQuery

from random_utils import *
from fixtures import new_notification_value


def test_insert():
    insert_values = [random_notification_insert_value() for _ in range(0, 20)]
    notifications.insert(insert_values)

    user_id = insert_values[0][1]

    lst = notifications.list_all(user_id, PaginatedQuery(0, 10))
    assert len(lst) >= 1


def test_list_paginated_query(new_notification_value):
    req = PaginatedQuery(0, 10)
    notifs = notifications.list_all(new_notification_value[1], req)

    assert len(notifs) >= 1


def test_list_ranged_query(new_notification_value):
    now = datetime.now()
    before = now.replace(year=2018)
    req = RangeQuery(before, now)
    notifs = notifications.list_all(new_notification_value[1], req)

    assert len(notifs) >= 1
