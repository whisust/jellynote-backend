import random, string
import pytest
from random_utils import *


@pytest.fixture(scope='function')
def new_user():
    from persist import users
    req = random_user_creation_request()
    yield users.insert(req)
