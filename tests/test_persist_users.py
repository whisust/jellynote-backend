import pytest
from persist import users
from datetime import datetime
from random_utils import *
from fixtures import new_user


def test_user_insert():
    req = random_user_creation_request()
    user = users.insert(req)

    assert user is not None
    assert user.name == req.name
    assert user.email == req.email
    assert user.instruments == req.instruments
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_list_all(new_user):
    lst = users.list_all(10)
    assert len(lst) <= 10
    assert new_user in lst
