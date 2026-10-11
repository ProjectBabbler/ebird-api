import unittest

from ebird.api.requests.validation import clean_locale


class CleanLocaleTests(unittest.TestCase):
    """Tests for the clean_locale validation function."""

    def test_case_corrected(self):
        self.assertEqual("en_US", clean_locale("EN_us"))

    def test_invalid_code(self):
        self.assertRaises(ValueError, clean_locale, "enUS")
