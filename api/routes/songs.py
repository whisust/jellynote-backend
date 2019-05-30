from flask import request, make_response, Blueprint

from models.errors import map_error, NotFoundError
from models.jellynote import SongId
from models.requests import SongCreationRequestSchema, SongUpdateRequestSchema
from persist import songs
from routes.utils import json_response

songs_bp = Blueprint('songs', __name__)


@songs_bp.route('', methods=['POST'])
def index():
    return create_song(request.json)


@songs_bp.route('/<int:song_id>', methods=['PUT', 'DELETE', 'GET'])
def song(song_id: int):
    s_id = SongId(song_id)
    if request.method == 'PUT':
        return update_song(s_id, request.json)
    elif request.method == 'DELETE':
        return delete_song(s_id)
    else:
        return get_song(s_id)


def get_song(song_id: SongId):
    try:
        song = songs.find(song_id)
        if song is None:
            response, code = (NotFoundError("song_id " + str(song_id) + " not found"), 404)
        else:
            response, code = song, 200
    except Exception as e:
        response, code = map_error(e)
    return json_response(response, code)


def delete_song(song_id: SongId):
    try:
        songs.delete(song_id)
        return '', 204
    except Exception as e:
        return map_error(e)


def update_song(song_id, data):
    try:
        req = SongUpdateRequestSchema.load(data)
        req.validate()
        song = songs.find(song_id)
        if song is None:
            response, code = (NotFoundError("song_id " + str(song_id) + " not found"), 404)
        else:
            updated = songs.update(song_id, req)
            response, code = updated, 200
    except Exception as e:
        response, code = map_error(e)
    return json_response(response, code)


def create_song(data):
    try:
        req = SongCreationRequestSchema.load(data)
        req.validate()
        song = songs.insert(req)
        response, code = song, 200
    except Exception as e:
        response, code = map_error(e)
    return json_response(response, code)
