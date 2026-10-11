import unittest

from ebird.api.requests.validation import clean_categories


class CleanCategoryTests(unittest.TestCase):
    """Tests for the clean_category validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual(["species"], clean_categories("Species"))

    def test_comma_separated_list(self):
        self.assertListEqual(["species", "form"], clean_categories("species,form"))
