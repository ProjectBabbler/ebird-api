import unittest

from ebird.api.requests.validation import clean_provisional


class CleanProvisionalTests(unittest.TestCase):
    """Tests for the clean_provisional validation function."""

    def test_converts_bool(self):
        self.assertEqual("true", clean_provisional(True))
        self.assertEqual("false", clean_provisional(False))

    def test_converts_integer(self):
        self.assertEqual("true", clean_provisional(1))
        self.assertEqual("false", clean_provisional(0))
