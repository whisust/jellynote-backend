from datetime import datetime

import pytest
from fixtures import new_song
from persist import songs
from random_utils import random_song_creation_request, random_song_update_request


def test_insert():
    req = random_song_creation_request()
    song = songs.insert(req)

    assert song.title == req.title
    assert song.instruments == req.instruments
    assert isinstance(song.created_at, datetime)
    assert isinstance(song.updated_at, datetime)


def test_find(new_song):
    song = songs.find(new_song.id)

    assert song == new_song


def test_find_none(new_song):
    song = songs.find(0)

    assert song is None


def test_update(new_song):
    req = random_song_update_request()
    updated_song = songs.update(new_song.id, req)

    assert updated_song.title == req.title
    assert updated_song.updated_at > new_song.updated_at
    assert updated_song.created_at == new_song.created_at
    assert updated_song.instruments == new_song.instruments


def test_list_all(new_song):
    song_list = songs.list_all(2)

    assert len(song_list) <= 2
    assert new_song in song_list


def test_delete(new_song):
    songs.delete(new_song.id)

    song = songs.find(new_song.id)
    assert song is None
