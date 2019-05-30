import pytest
import api
from api import validators
from api.models.jellynote import Instrument
import re


class TestSerdeMethods(object):

    def test_validate_not_empty_nominal(self):
        validator = validators.non_empty('name')
        assert validator('guitar') == 'guitar'

    def test_validate_not_empty_failure(self):
        with pytest.raises(ValueError):
            validator = validators.non_empty('name')
            validator('')

    def test_validate_regex_nominal(self):
        validator = validators.match_regex('number', re.compile(r'[0-9]+'), '1234')
        assert validator('5555') == '5555'

    def test_decode_enum_iterable_failure(self):
        with pytest.raises(ValueError):
            validator = validators.match_regex('number', re.compile(r'[0-9]+'), '1234')
            validator('not a number')
