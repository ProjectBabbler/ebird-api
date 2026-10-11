import unittest

from ebird.api.requests.validation import clean_hotspot


class CleanHotspotTests(unittest.TestCase):
    """Tests for the clean_hotspot validation function."""

    def test_converts_bool(self):
        self.assertEqual("true", clean_hotspot(True))
        self.assertEqual("false", clean_hotspot(False))

    def test_converts_integer(self):
        self.assertEqual("true", clean_hotspot(1))
        self.assertEqual("false", clean_hotspot(0))
