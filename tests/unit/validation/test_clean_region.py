import unittest

from ebird.api.requests.validation import clean_region


class CleanRegionTests(unittest.TestCase):
    """Tests for the clean_region validation function."""

    def test_codes_are_correct_case(self):
        self.assertEqual("US", clean_region("us"))
        self.assertEqual("US-NV", clean_region("us-nv"))
        self.assertEqual("world", clean_region("WORLD"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_region, "US-")
