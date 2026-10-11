import unittest

from ebird.api.requests.validation import clean_areas


class CleanAreasTests(unittest.TestCase):
    """Tests for the clean_areas function."""

    def test_comma_separated_string(self):
        self.assertEqual(["US", "CA", "MX"], clean_areas("US,CA,MX"))

    def test_list(self):
        self.assertEqual(["US", "CA", "MX"], clean_areas(["US", "CA", "MX"]))

    def test_cannot_mix_types(self):
        self.assertRaises(ValueError, clean_areas, ["US", "US-NV"])

    def test_limit_list_to_ten_locations(self):
        self.assertRaises(ValueError, clean_areas, ["US-NV"] * 11)
