from unittest import TestCase

from ebird.api.requests.hotspots import REGION_HOTSPOTS_URL, get_hotspots
from tests.unit.mixins import BackTestsMixin, HeaderTestsMixin


class GetHotspotsTests(TestCase, BackTestsMixin, HeaderTestsMixin):
    """Tests for the get_hotspots() API call."""

    def get_callable(self):
        return get_hotspots

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "region": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_code(self):
        url = self.api_call()[0]
        self.assertEqual(REGION_HOTSPOTS_URL % "US-NV", url)
