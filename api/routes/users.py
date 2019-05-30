from flask import request, make_response, Blueprint

from models.errors import map_error, NotFoundError
from models.jellynote import UserId
from models.requests import UserCreationRequestSchema, UserUpdateRequestSchema
from persist import users, InsertionError
from .utils import json_response

users_bp = Blueprint('users', __name__)

user_list = []


@users_bp.route('', methods=['POST'])
def index():
    return create_user(request.json)


@users_bp.route('/<int:user_id>', methods=['PUT', 'DELETE'])
def user(user_id):
    if request.method == 'PUT':
        return "Not implemented " + str(user_id), 500
    else:
        return "Still not implemented " + str(user_id), 500


def create_user(data):
    try:
        user_req = UserCreationRequestSchema.load(data)
        user_req.validate()
        new_user = users.insert(user_req)
        (response, code) = (new_user, 200)
    except InsertionError as e:
        response, code = (e, 409)
    except Exception as e:
        response, code = map_error(e)
    resp = make_response(response.to_json(), code)
    resp.headers['Content-Type'] = "application/json"
    return json_response(response, code)
