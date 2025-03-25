import unittest

from ebird.api.validation import clean_observation_rank


class CleanObservationRankTests(unittest.TestCase):
    """Tests for the rank validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual("mrec", clean_observation_rank("Mrec"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_observation_rank, "none")
