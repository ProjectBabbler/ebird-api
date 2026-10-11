import unittest

from ebird.api.requests.validation import clean_location


class CleanLocationTests(unittest.TestCase):
    """Tests for the clean_location function."""

    def test_code_is_upper_case(self):
        self.assertEqual("L123456", clean_location("l123456"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_location, "S227544")
