import unittest

from ebird.api.requests.validation import clean_codes


class CleanCodesTests(unittest.TestCase):
    """Tests for the clean_codes validation function."""

    def test_single_code_returns_list(self):
        self.assertEqual(["abc"], clean_codes("abc"))

    def test_comma_separated_list(self):
        self.assertEqual(["a", "b", "c"], clean_codes("a, b, c"))

    def test_list(self):
        self.assertEqual(["a", "b", "c"], clean_codes(["a", "b", "c"]))
