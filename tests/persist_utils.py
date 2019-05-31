from random_utils import random_user_creation_request, random_song_creation_request, random_notification_insert_value


def new_user():
    from persist import users
    req = random_user_creation_request()
    return users.insert(req)


def new_song():
    from persist import songs
    req = random_song_creation_request()
    return songs.insert(req)


def new_notification_value():
    from persist import notifications
    value = random_notification_insert_value()
    notifications.insert([value])
    return value
