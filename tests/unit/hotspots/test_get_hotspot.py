from unittest import TestCase

from ebird.api.requests.hotspots import HOTSPOT_INFO_URL, get_hotspot
from tests.unit.mixins import HeaderTestsMixin


class GetHotspotTests(TestCase, HeaderTestsMixin):
    """Tests for the get_hotspot() API call."""

    def get_callable(self):
        return get_hotspot

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "loc_id": "L123456",
        }
        params.update(kwargs)
        return params

    def test_url_contains_location_code(self):
        url = self.api_call()[0]
        self.assertEqual(HOTSPOT_INFO_URL % "L123456", url)

    def test_invalid_location_code_raises_error(self):
        self.api_raises(ValueError, loc_id="123456")
