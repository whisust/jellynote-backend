from flask import request, make_response, Blueprint
from models.jellynote import User
from models.requests import UserCreationRequest, UserCreationRequestSchema
from models.errors import BaseError
from marshmallow.exceptions import ValidationError
from datetime import datetime
import traceback, sys

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
    response, code = "{}", 500
    try:
        user_req = UserCreationRequestSchema.load(data)
        user_req.validate()
        print(user_req)
        response = User(0, user_req.name, user_req.email, datetime.now(), datetime.now(), list(user_req.instruments))
        code = 200
    except (ValueError, ValidationError, KeyError) as e:
        response, code = (BaseError(str(e.args)), 400)
    except Exception as e:
        traceback.print_exc(limit=10, file=sys.stdout)
        response, code = (BaseError(str(e)), 500)
    resp = make_response(response.to_json(), code)
    resp.headers['Content-Type'] = "application/json"
    return resp
