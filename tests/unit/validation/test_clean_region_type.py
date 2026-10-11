import unittest

from ebird.api.requests.validation import clean_region_type


class CleanRegionTypeTests(unittest.TestCase):
    """Tests for the clean_region_type function."""

    def test_codes_are_lower_case(self):
        self.assertEqual("country", clean_region_type("Country"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_region_type, "L123456")
