import random, string
import pytest

from random_utils import *


@pytest.fixture(scope='function')
def new_user():
    from persist import users
    req = random_user_creation_request()
    yield users.insert(req)


@pytest.fixture(scope='function')
def new_song():
    from persist import songs
    req = random_song_creation_request()
    yield songs.insert(req)


@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield client

    ctx.pop()