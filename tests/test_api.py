import pytest
from api.app import flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()
    yield client


def test_user_creation(client):
    result = client.post('/users', json={
        "name": "testestes",
        "email": "email@me.com",
        "instruments": ["guitar", "piano"]
    })

    result
    assert False
