import pytest
from app import create_app
from random_utils import *


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield client

    ctx.pop()


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
