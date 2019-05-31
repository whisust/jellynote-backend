import pytest

from models.jellynote import UserId
from persist import users, UpdateError, InsertionError
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


def test_user_insert_conflict(new_user):
    req = UserCreationRequest(name=random_string(10), email=new_user.email, instruments=random_enum_list(Instrument))
    with pytest.raises(InsertionError):
        users.insert(req)


def test_list_all(new_user):
    lst = users.list_all(10)
    assert len(lst) <= 10
    assert new_user in lst


def test_find(new_user):
    user = users.find(new_user.id)
    assert user == new_user


def test_find_if_none():
    user = users.find(UserId(0))
    assert user is None


def test_update(new_user):
    req = random_user_update_request()
    updated_user = users.update(new_user.id, req)
    assert updated_user.id == new_user.id
    if req.name is not None:
        assert updated_user.name == req.name

    if req.email is not None:
        assert updated_user.email == req.email

    if req.instruments is not None:
        assert updated_user.instruments == req.instruments

    assert updated_user.updated_at > new_user.updated_at


def test_update_conflict(new_user):
    new_user_req = random_user_creation_request()
    second_user = users.insert(new_user_req)

    req = UserUpdateRequest(name=None, email=second_user.email, instruments=None)
    with pytest.raises(UpdateError):
        users.update(new_user.id, req)


def test_delete_user(new_user):
    users.delete(new_user.id)

    u = users.find(new_user.id)
    assert u is None


def test_list_by_instrument(new_user):
    us = users.list_by_instruments(new_user.instruments)
    instruments_set = set(new_user.instruments)
    for u in us:
        assert not set(u.instruments).isdisjoint(instruments_set)