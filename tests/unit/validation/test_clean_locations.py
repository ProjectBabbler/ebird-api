import unittest

from ebird.api.requests.validation import clean_locations


class CleanLocationsTests(unittest.TestCase):
    """Tests for the clean_locations function."""

    def test_comma_separated_string(self):
        self.assertEqual(["L006", "L007", "L008"], clean_locations("L006,L007,L008"))

    def test_list(self):
        self.assertEqual(
            ["L006", "L007", "L008"], clean_locations(["L006", "L007", "L008"])
        )

    def test_only_locations_are_allowed(self):
        self.assertRaises(ValueError, clean_locations, ["L006", "US-NV"])

    def test_limit_list_to_ten_locations(self):
        self.assertRaises(ValueError, clean_locations, ["L001"] * 11)
