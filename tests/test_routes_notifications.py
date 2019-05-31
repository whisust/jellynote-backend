from datetime import datetime

import pytest

from models.jellynote import Song
from random_utils import *
from fixtures import client
from persist import notifications


def test_notifications_retrieval_daterange(client):
    user_id = random.randint(0, 999999)
    req = random_notification_insert_values(30, user_id)
    notifications.insert(req)

    dt = datetime.now()
    dt1 = dt.replace(year=dt.year + 1).date()
    dt2 = dt.replace(year=dt.year - 1).date()
    date_range = dt2.isoformat() + '_' + dt1.isoformat()

    res = client.get('/notifications/' + str(user_id) + '?date-range=' + date_range)
    assert res.status_code == 200
    assert len(res.json["notifications"]) == 30
    assert res.headers['Content-Range'] == '*/30'


def test_notifications_retrieval_range(client):
    user_id = random.randint(0, 999999)
    req = random_notification_insert_values(20, user_id)
    notifications.insert(req)

    res = client.get('/notifications/' + str(user_id) + '?range=10_20')
    assert res.status_code == 200
    assert len(res.json["notifications"]) == 10


def test_notifications_retrieval_range_limited(client):
    user_id = random.randint(0, 999999)
    req = random_notification_insert_values(15, user_id)
    notifications.insert(req)

    res = client.get('/notifications/' + str(user_id) + '?range=10_20')
    assert res.status_code == 200
    assert len(res.json["notifications"]) == 5
    assert res.headers['Content-Range'] == '10-15/15'


def test_notifications_retrieval_no_range(client):
    user_id = random.randint(0, 999999)
    req = random_notification_insert_values(40, user_id)
    notifications.insert(req)

    res = client.get('/notifications/' + str(user_id))
    assert res.status_code == 200
    assert len(res.json["notifications"]) == 20
    assert res.headers['Content-Range'] == '0-20/40'
