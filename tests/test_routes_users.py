import pytest

from random_utils import *
from fixtures import client


def _or(a, b):
    return b if a is None else a


# POST /users

def test_user_creation(client):
    req = random_user_creation_request()
    instruments_as_str = [i.value for i in req.instruments]
    result = client.post('/users', json={
        "name": req.name,
        "email": req.email,
        "instruments": instruments_as_str
    })

    assert result.status_code == 200
    assert result.json["name"] == req.name
    assert result.json["email"] == req.email
    assert result.json["instruments"] == instruments_as_str
    assert result.json["created_at"] is not None
    assert result.json["updated_at"] is not None


def test_user_creation_bad_email(client):
    result = client.post('/users', json={
        "name": "testestes",
        "email": "aintamail",
        "instruments": ["guitar", "piano"]
    })

    assert result.status_code == 400
    assert result.json["message"] == "Invalid field : email is incorrect"


def test_user_creation_empty_name(client):
    result = client.post('/users', json={
        "name": "",
        "email": "email@me.com",
        "instruments": ["guitar", "piano"]
    })

    assert result.status_code == 400
    assert result.json["message"] == "Invalid field : name should not be empty"


def test_user_creation_empty_instruments(client):
    result = client.post('/users', json={
        "name": "john",
        "email": "email@me.com",
        "instruments": []
    })

    assert result.status_code == 400
    assert result.json["message"] == "Invalid field : instruments should not be empty"


def test_existing_user_creation_returns_conflict(client):
    req = random_user_creation_request()
    instruments_as_str = [i.value for i in req.instruments]
    _ = client.post('/users', json={
        "name": req.name,
        "email": req.email,
        "instruments": instruments_as_str
    })

    result = client.post('/users', json={
        "name": req.name,
        "email": req.email,
        "instruments": instruments_as_str
    })

    assert result.status_code == 409


# PUT /users/:id

def test_update_user_name(client):
    # should be in another fixture but flemme
    creation = random_user_creation_request()
    instruments_as_str = [i.value for i in creation.instruments]
    creation_result = client.post('/users', json={
        "name": creation.name,
        "email": creation.email,
        "instruments": instruments_as_str
    })

    user_id = creation_result.json["id"]
    name = "newname"
    update_result = client.put('/users/' + str(user_id), json={
        "name": name
    })

    assert update_result.status_code == 200
    assert update_result.json['name'] == name
    assert update_result.json['email'] == creation.email
    assert update_result.json['instruments'] == instruments_as_str


def test_update_user_email(client):
    # should be in another fixture but flemme
    creation = random_user_creation_request()
    instruments_as_str = [i.value for i in creation.instruments]
    creation_result = client.post('/users', json={
        "name": creation.name,
        "email": creation.email,
        "instruments": instruments_as_str
    })

    user_id = creation_result.json["id"]
    email = random_mail()
    update_result = client.put('/users/' + str(user_id), json={
        "email": email
    })

    assert update_result.status_code == 200
    assert update_result.json['name'] == creation.name
    assert update_result.json['email'] == email
    assert update_result.json['instruments'] == instruments_as_str


def test_update_user_instruments(client):
    # should be in another fixture but flemme
    creation = random_user_creation_request()
    creation_result = client.post('/users', json={
        "name": creation.name,
        "email": creation.email,
        "instruments": [Instrument.Guitar.value]
    })

    user_id = creation_result.json["id"]
    update_result = client.put('/users/' + str(user_id), json={
        "instruments": [Instrument.Violin.value]
    })

    assert update_result.status_code == 200
    assert update_result.json['name'] == creation.name
    assert update_result.json['email'] == creation.email
    assert update_result.json['instruments'] == [Instrument.Violin.value]


def test_update_user(client):
    # should be in another fixture but flemme
    creation = random_user_creation_request()
    instruments_as_str = [i.value for i in creation.instruments]
    creation_result = client.post('/users', json={
        "name": creation.name,
        "email": creation.email,
        "instruments": instruments_as_str
    })

    user_id = creation_result.json["id"]
    req = random_user_update_request()
    name = random_string(5) # we force the name to ensure no 3 emtpy params
    updated_instruments_as_str = [i.value for i in req.instruments] if req.instruments is not None else None
    update_result = client.put('/users/' + str(user_id), json={
        "name": name,
        "email": req.email,
        "instruments": updated_instruments_as_str
    })

    assert update_result.status_code == 200
    assert update_result.json['name'] == name
    assert update_result.json['email'] == _or(req.email, creation.email)
    assert update_result.json['instruments'] == _or(updated_instruments_as_str, instruments_as_str)


def test_update_user_conflict(client):
    """Create two users, try to update email of first one with the second user's email -> conflict"""
    # should be in another fixture but flemme
    creation = random_user_creation_request()
    instruments_as_str = [i.value for i in creation.instruments]
    creation_result = client.post('/users', json={
        "name": creation.name,
        "email": creation.email,
        "instruments": instruments_as_str
    })

    creation2 = random_user_creation_request()
    instruments_as_str = [i.value for i in creation2.instruments]
    creation_result2 = client.post('/users', json={
        "name": creation2.name,
        "email": creation2.email,
        "instruments": instruments_as_str
    })

    user_id = creation_result.json["id"]
    req = UserUpdateRequest(name=None, email=creation2.email, instruments=None)
    update_result = client.put('/users/' + str(user_id), json={
        "email": req.email,
    })

    assert update_result.status_code == 409
