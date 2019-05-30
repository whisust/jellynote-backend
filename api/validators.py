from re import Pattern
from typing import Optional


def non_empty(field: str):
    def _test_non_empty(value: str):
        if len(value) == 0:
            raise ValueError(field + " should not be empty")
        else:
            return value

    return _test_non_empty


def match_regex(field: str, regex: Pattern, example: Optional[str] = None):
    def _test_regex(value: str):
        if regex.match(value) is None:
            msg = field + " is incorrect"
            if example is not None:
                msg += ". Example: " + example
            raise ValueError(msg)
        else:
            return value

    return _test_regex
