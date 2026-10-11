import unittest

from ebird.api.requests.validation import Transform, clean_code


class CleanCodeTests(unittest.TestCase):
    """Tests for the clean_code validation function."""

    def test_whitespace_removed(self):
        self.assertEqual("abc", clean_code(" abc "))

    def test_convert_to_lowercase(self):
        self.assertEqual("abc", clean_code("ABC", transform=Transform.LOWER))

    def test_convert_to_uppercase(self):
        self.assertEqual("ABC", clean_code("abc", transform=Transform.UPPER))

    def test_code_must_be_string(self):
        self.assertRaises(ValueError, clean_code, 1)
