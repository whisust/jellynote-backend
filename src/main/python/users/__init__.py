from flask import Blueprint
from dataclasses import *
from dataclasses_json import dataclass_json

users_bp = Blueprint('users', __name__)


@dataclass_json
@dataclass
class User:
    '''User representation'''
    id: int
    name: str
    mail: str
    created_at: float
    instruments: list


import users.routes
