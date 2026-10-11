import unittest

from ebird.api.requests.validation import clean_ordering


class CleanOrderingTests(unittest.TestCase):
    """Tests for the clean_ordering validation function."""

    def test_code_is_lower_case(self):
        self.assertEqual("ebird", clean_ordering("eBird"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_ordering, "none")
