import unittest

from ebird.api.validation import clean_areas


class CleanAreasTests(unittest.TestCase):
    """Tests for the clean_areas function."""

    def test_comma_separated_list(self):
        self.assertEqual(['US', 'CA', 'MX'], clean_areas('us,ca,mx'))

    def test_cannot_mix_types(self):
        self.assertRaises(ValueError, clean_areas, ['US', 'US-NV'])
