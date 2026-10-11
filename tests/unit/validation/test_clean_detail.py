import unittest

from ebird.api.requests.validation import clean_detail


class CleanDetailTests(unittest.TestCase):
    """Tests for the clean_detail validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual("full", clean_detail("Full"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_detail, "none")
