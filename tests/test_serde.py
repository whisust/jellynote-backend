import pytest
import api
from api import serde
from api.models.jellynote import Instrument


class TestSerdeMethods(object):

    def test_decode_enum_nominal(self):
        decoder = serde.decode_enum(Instrument)
        assert decoder('guitar') == Instrument.Guitar

    def test_decode_enum_failure(self):
        with pytest.raises(ValueError):
            decoder = serde.decode_enum(Instrument)
            decoder('Mayonaise')

    def test_decode_enum_iterable_nominal(self):
        decoder = serde.decode_enum_iterable(Instrument)
        assert decoder(['guitar', 'Violin']) == [Instrument.Guitar, Instrument.Violin]

    def test_decode_enum_iterable_failure(self):
        with pytest.raises(ValueError):
            decoder = serde.decode_enum_iterable(Instrument)
            decoder(['guitar', 'Mayonaise', 'violin'])
