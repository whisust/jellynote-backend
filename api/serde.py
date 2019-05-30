from typing import Callable


def format_capitalize(value: str):
    return value.lower().capitalize()


def decode_enum(enum_type, value_formatter=format_capitalize):
    """
    Generate a function that either find a case insensitive version of an item or raise a ValueError
    :param enum_type: the enum class used for decoding
    :param value_formatter: function to use to transform the value on a valid representation of an item
    :return: a function to decode a string into an item of the enumeration
    """

    def _decode_or_error(value):
        return enum_type(value_formatter(str(value)))

    return _decode_or_error


def decode_enum_iterable(enum_type, format_value=format_capitalize):
    """
    Generate a function that either find a case insensitive version of a list of items or raise a ValueError
    :param enum_type: the enum class used for decoding
    :param format_value: function to use to transform a value on a valid representation of an item
    :return: a function to decode an array of strings into a list of items
    """

    def _decode_or_error(values):
        if values is None:
            return None
        return [enum_type(format_value(str(value))) for value in values]

    return _decode_or_error


def encode_enum(item):
    return item.value


def encode_enum_iterable(items):
    if items is None:
        return None
    return [encode_enum(item) for item in items]
