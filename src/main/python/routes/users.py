from flask import request, make_response, Blueprint
from models import User
from datetime import datetime

users_bp = Blueprint('users', __name__)

user_list = []


@users_bp.route('/', methods=['POST'])
def index():
    return create_user(request.json)


@users_bp.route('/<int:user_id>', methods=['PUT', 'DELETE'])
def user(user_id):
    if request.method == 'PUT':
        return "Not implemented " + str(user_id), 500
    else:
        return "Still not implemented " + str(user_id), 500


def create_user(data):
    user_list.append(
        User(id=len(user_list), name=data["name"], mail=data["mail"], created_at=datetime.now(), instruments=['ins1', 'ins2']))
    resp = make_response(user_list[-1].to_json(), 200)
    resp.headers['Content-Type'] = "application/json"
    return resp
