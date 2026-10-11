import unittest

from ebird.api.requests.validation import clean_area


class CleanAreaTests(unittest.TestCase):
    """Tests for the clean_area function."""

    def test_codes_are_upper_case(self):
        self.assertEqual("US", clean_area("us"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_area, "world")
