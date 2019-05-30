from re import Pattern
from typing import Optional


def non_empty(field: str):
    def _test_non_empty(value: str):
        if value is None or len(value) == 0:
            raise ValueError(field + " should not be empty")
        else:
            return value

    return _test_non_empty


def non_all_empty(fields: list):
    def _test_non_empty(values: str):
        non_empty_values = [v for v in values if v is not None]
        if len(non_empty_values) == 0:
            raise ValueError("Require at least one of " + ', '.join(fields))
        else:
            return non_empty_values

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
