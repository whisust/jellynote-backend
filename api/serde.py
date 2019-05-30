from models import AutoName
from typing import Callable


def format_capitalize(value: str):
    return value.lower().capitalize()


def decode_enum(enum_type: AutoName, format_value: Callable[[str], str] = format_capitalize):
    """
    Generate a function that either find a case insensitive version of an item or raise a ValueError
    :param enum_type: the enum class used for decoding
    :param format_value: function to use to transform the value on a valid representation of an item
    :return: a function to decode a string into an item of the enumeration
    """

    def _decode_or_error(value):
        return enum_type(format_value(str(value)))

    return _decode_or_error


def decode_enum_iterable(enum_type: AutoName, format_value: Callable[[str], str] = format_capitalize):
    """
    Generate a function that either find a case insensitive version of a list of items or raise a ValueError
    :param enum_type: the enum class used for decoding
    :param format_value: function to use to transform a value on a valid representation of an item
    :return: a function to decode an array of strings into a list of items
    """

    def _decode_or_error(values):
        return [enum_type(format_value(str(value))) for value in values]

    return _decode_or_error
