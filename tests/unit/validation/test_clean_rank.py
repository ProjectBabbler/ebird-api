import unittest

from ebird.api.requests.validation import clean_rank


class CleanRankTests(unittest.TestCase):
    """Tests for the deprecated clean_rank validation function."""

    def test_deprecation_warning_is_raised(self):
        with self.assertWarns(DeprecationWarning):
            clean_rank("spp")

    def test_codes_are_lower_case(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual("spp", clean_rank("SPP"))

    def test_invalid_code_raises_error(self):
        with self.assertWarns(DeprecationWarning):
            self.assertRaises(ValueError, clean_rank, "none")
