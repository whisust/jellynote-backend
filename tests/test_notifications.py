from persist import songs, users, notifications as notifs, PaginatedQuery
import pytest
from random_utils import *
from persist_utils import *
from models.jellynote import *
from notifications import generate_notifications


def test_notifications_generated():
    instruments = random_enum_list(Instrument, 2, len(list(Instrument)) - 1)
    req = random_song_creation_request(instruments)
    song = songs.insert(req)

    # only one instrument in notif
    req1 = random_user_creation_request(instruments[0:1])
    user1 = users.insert(req1)

    # all instruments in notif
    req2 = random_user_creation_request(instruments)
    user2 = users.insert(req2)

    # not notified
    other_instruments = set(list(Instrument)).difference(set(instruments))
    req3 = random_user_creation_request(list(other_instruments))
    user3 = users.insert(req3)

    generate_notifications(song)

    notifs1 = notifs.list_all(user1.id, PaginatedQuery(0, 2))
    notifs2 = notifs.list_all(user2.id, PaginatedQuery(0, 2))
    notifs3 = notifs.list_all(user3.id, PaginatedQuery(0, 2))

    assert len(notifs1) == 1
    assert notifs1[0].song_id == song.id

    assert len(notifs2) == 1
    assert notifs2[0].song_id == song.id

    assert len(notifs3) == 0
