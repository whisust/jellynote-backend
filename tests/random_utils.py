import random, string
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
