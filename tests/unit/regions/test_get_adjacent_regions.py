from unittest import TestCase

from ebird.api.requests.regions import (
    ADJACENT_REGIONS_URL,
    get_adjacent_regions,
)
from tests.unit.mixins import HeaderTestsMixin


class GetAdjacentRegionTests(TestCase, HeaderTestsMixin):
    """Tests for the get_adjacent_regions() API call."""

    def get_callable(self):
        return get_adjacent_regions

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "region": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(ADJACENT_REGIONS_URL % "US-NV", url)
