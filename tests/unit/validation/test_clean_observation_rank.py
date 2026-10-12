import unittest

from ebird.api.requests.validation import clean_observation_rank


class CleanObservationRankTests(unittest.TestCase):
    """Tests for the clean_observation_rank validation function."""

    def test_codes_are_lower_case(self):
        self.assertEqual("mrec", clean_observation_rank("MREC"))
        self.assertEqual("create", clean_observation_rank("Create"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_observation_rank, "none")
