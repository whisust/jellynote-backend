import pytest
from api.app import create_app


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
    result = client.post('/users', json={
        "name": "testestes",
        "email": "email@me.com",
        "instruments": ["guitar", "piano"]
    })

    assert result.status_code == 200
    assert result.json["name"] == "testestes"
    assert result.json["email"] == "email@me.com"
    assert result.json["instruments"] == ['Guitar', 'Piano']
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
