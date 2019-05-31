import random, string

from models.jellynote import SongId, UserId
from models.requests import *


def random_string(size: int) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def random_mail() -> str:
    return random_string(10) + '@' + random_string(6) + '.' + random_string(2)


def random_enum(clazz):
    return random.choice(list(clazz))


def random_enum_list(clazz):
    return random.choices(list(clazz))


def random_user_creation_request():
    return UserCreationRequest(random_string(10), random_mail(), random_enum_list(Instrument))


def random_optional(filled_value):
    return random.choice([None, filled_value])


def random_user_update_request():
    return UserUpdateRequest(random_optional(random_string(10)),
                             random_optional(random_mail()),
                             random_optional(random_enum_list(Instrument)))


def random_song_creation_request():
    return SongCreationRequest(random_string(10), random_enum_list(Instrument))


def random_song_update_request():
    return SongUpdateRequest(random_string(10))


def random_notification_insert_value(user_id=None):
    return SongId(random.randint(1, 99999)), user_id if user_id is not None else UserId(random.randint(1, 99999)), random_string(30)


def random_notification_insert_values(count, user_id=None):
    return [random_notification_insert_value(user_id) for _ in range(0, count)]
