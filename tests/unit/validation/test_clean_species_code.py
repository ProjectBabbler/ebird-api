import unittest

from ebird.api.requests.validation import clean_species_code


class CleanLocationTests(unittest.TestCase):
    """Tests for the functions used for validating species_codes."""

    def test_code_is_lower_case(self):
        self.assertEqual("cangoo", clean_species_code("CANGOO"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_species_code, "none")
