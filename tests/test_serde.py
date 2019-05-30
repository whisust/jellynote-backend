import unittest
import serde
from models.jellynote import Instrument


class TestSerdeMethods(unittest.TestCase):

    def test_decode_enum_nominal(self):
        decoder = serde.decode_enum(Instrument)
        self.assertEqual(decoder('guitar'), Instrument.Guitar)

    def test_decode_enum_failure(self):
        with self.assertRaisesRegex(ValueError, "'Mayonaise' is not a valid Instrument"):
            decoder = serde.decode_enum(Instrument)
            decoder('Mayonaise')

    def test_decode_enum_iterable_nominal(self):
        decoder = serde.decode_enum_iterable(Instrument)
        self.assertEqual(decoder(['guitar', 'Violin']), [Instrument.Guitar, Instrument.Violin])

    def test_decode_enum_iterable_failure(self):
        with self.assertRaisesRegex(ValueError, "'Mayonaise' is not a valid Instrument"):
            decoder = serde.decode_enum_iterable(Instrument)
            decoder(['guitar', 'Mayonaise', 'violin'])


if __name__ == '__main__':
    unittest.main()
