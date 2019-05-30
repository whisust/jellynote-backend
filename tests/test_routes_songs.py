import pytest

from models.jellynote import Song
from random_utils import *
from fixtures import client


def _or(a, b):
    return b if a is None else a


def new_song_from_api(client, req: Optional[SongCreationRequest] = None):
    _req = random_song_creation_request() if req is None else req
    instruments_as_str = [i.value for i in _req.instruments]
    res = client.post('/songs', json={
        "title": _req.title,
        "instruments": instruments_as_str
    })
    return Song(id=res.json["id"], title=res.json["title"], instruments=_req.instruments,
                created_at=res.json["created_at"], updated_at=res.json["updated_at"])


def test_song_creation(client):
    req = random_song_creation_request()
    instruments_as_str = [i.value for i in req.instruments]
    res = client.post('/songs', json={
        "title": req.title,
        "instruments": instruments_as_str
    })

    assert res.status_code == 200
    assert res.json["title"] == req.title
    assert res.json["instruments"] == instruments_as_str


def test_song_creation_empty_instruments(client):
    req = random_song_creation_request()
    res = client.post('/songs', json={
        "title": req.title,
        "instruments": []
    })

    assert res.status_code == 400


def test_update_song(client):
    song = new_song_from_api(client)
    req = random_song_update_request()
    res = client.put('/songs/' + str(song.id), json={
        "title": req.title
    })

    assert res.status_code == 200
    assert res.json["id"] == song.id
    assert res.json["title"] == req.title
    assert res.json["instruments"] == [i.value for i in song.instruments]
    assert res.json["updated_at"] > song.updated_at
    assert res.json["created_at"] == song.created_at


def test_get_song(client):
    song = new_song_from_api(client)
    res = client.get('/songs/' + str(song.id))

    assert res.status_code == 200
    assert res.json["id"] == song.id


def test_get_song_none(client):
    res = client.get('/songs/' + str(0))

    assert res.status_code == 404


def test_delete_song(client):
    song = new_song_from_api(client)
    res = client.delete('/songs/' + str(song.id))

    assert res.status_code == 204

    res = client.get('/songs/' + str(song.id))
    assert res.status_code == 404
