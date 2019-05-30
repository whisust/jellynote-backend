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
        (response, code) = (User(0, user_req.name, user_req.email, user_req.instruments,
                                 created_at=datetime.now(),
                                 updated_at=datetime.now()),
                            200)
    except ValueError as e:  # //  "instruments": ["guitar", "piano"]
        response, code = (BaseError("Invalid field : " + e.args[0]), 400)
    except KeyError as e:
        response, code = (BaseError("Missing field : " + e.args[0]), 400)
    except ValidationError as e:
        response, code = (BaseError(e.args), 400)
    # except Exception as e:
    #     traceback.print_exc(limit=10, file=sys.stdout)
    #     response, code = (BaseError(str(e)), 500)
    resp = make_response(response.to_json(), code)
    resp.headers['Content-Type'] = "application/json"
    return resp
