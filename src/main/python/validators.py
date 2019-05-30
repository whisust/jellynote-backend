from re import Pattern


def non_empty(field: str):
    def _test_non_empty(value: str):
        if len(value) == 0:
            raise ValueError(field + " should not be empty")
        else:
            return value

    return _test_non_empty


def match_regex(field: str, regex: Pattern, example: str):
    def _test_regex(value: str):
        if regex.match(value) is None:
            raise ValueError(field + " is incorrect. Example: " + example)
        else:
            return value

    return _test_regex
