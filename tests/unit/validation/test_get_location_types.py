import unittest

from ebird.api.requests.validation import get_location_types


class GetLocationTypesTests(unittest.TestCase):
    """Tests for the get_location_types function."""

    def test_list(self):
        results = get_location_types(["US", "US-NV", "US-NV-11", "L123456"])
        expected = ["country", "subnational1", "subnational2", "location"]
        self.assertListEqual(sorted(results), sorted(expected))

    def test_invalid_list(self):
        results = get_location_types(["U", "US-NV-"])
        expected = [None]
        self.assertListEqual(sorted(results), sorted(expected))

    def test_empty_list(self):
        results = get_location_types([])
        self.assertListEqual(results, [])

    def test_no_duplicates(self):
        results = get_location_types(["US", "US", "US-NV-11", "US-NV-11"])
        expected = ["country", "subnational2"]
        self.assertListEqual(sorted(results), sorted(expected))
