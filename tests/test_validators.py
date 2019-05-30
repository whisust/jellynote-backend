import re

import pytest

import validators


class TestValidatorsMethods(object):

    def test_validate_not_empty_nominal(self):
        assert validators.non_empty('name')('guitar') == 'guitar'

    def test_validate_not_empty_failure(self):
        with pytest.raises(ValueError):
            validators.non_empty('name')('')

    def test_validate_regex_nominal(self):
        validator = validators.match_regex('number', re.compile(r'[0-9]+'), '1234')
        assert validator('5555') == '5555'

    def test_decode_enum_iterable_failure(self):
        with pytest.raises(ValueError):
            validator = validators.match_regex('number', re.compile(r'[0-9]+'), '1234')
            validator('not a number')
