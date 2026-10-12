import unittest

from ebird.api.requests.validation import clean_observer_rank


class CleanObserverRankTests(unittest.TestCase):
    """Tests for the clean_observer_rank validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual("spp", clean_observer_rank("SPP"))
        self.assertEqual("cl", clean_observer_rank("Cl"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_observer_rank, "none")
