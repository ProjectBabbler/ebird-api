import unittest

from ebird.api.requests import constants
from ebird.api.requests.validation import clean_observation_rank

class CleanObservationRankTests(unittest.TestCase):
    """Tests for the rank validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual(clean_observation_rank("Mrec"), "mrec")

    def test_invalid_code_raises_error(self):
        with self.assertRaises(ValueError) as value_error:
            clean_observation_rank("none")
        self.assertEqual(str(value_error.exception), f"Value for 'rank', none, must be in the set {constants.HISTORIC_RANKING_TYPES}.")
