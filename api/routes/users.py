from flask import request, make_response, Blueprint

from models.errors import map_error, NotFoundError
from models.jellynote import UserId
from models.requests import UserCreationRequestSchema, UserUpdateRequestSchema
from persist import users, InsertionError, UpdateError
from .utils import json_response

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['POST'])
def index():
    return create_user(request.json)


@users_bp.route('/<int:user_id>', methods=['PUT', 'DELETE', 'GET'])
def user(user_id):
    us_id = UserId(user_id)
    if request.method == 'PUT':
        return update_user(us_id, request.json)
    elif request.method == 'DELETE':
        return delete_user(us_id)
    else:
        return get_user(us_id)


def get_user(user_id: UserId):
    try:
        user = users.find(user_id)
        if user is None:
            response, code = (NotFoundError("user_id " + str(user_id) + " not found"), 404)
        else:
            response, code = user, 200
    except Exception as e:
        response, code = map_error(e)
    return json_response(response, code)


def delete_user(user_id: UserId):
    try:
        users.delete(user_id)
        return '', 204
    except Exception as e:
        return map_error(e)


def update_user(user_id: UserId, data):
    try:
        user_req = UserUpdateRequestSchema.load(data)
        user_req.validate()
        user = users.find(user_id)
        if user is None:
            response, code = (NotFoundError("user_id " + str(user_id) + " not found"), 404)
        else:
            updated_user = users.update(user_id, user_req)
            response, code = (updated_user, 200)
    except UpdateError as e:
        response, code = (e, 409)
    except Exception as e:
        response, code = map_error(e)
    return json_response(response, code)


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
