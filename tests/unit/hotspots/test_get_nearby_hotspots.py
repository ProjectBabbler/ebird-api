from unittest import TestCase

from ebird.api.requests.hotspots import (
    NEARBY_HOTSPOTS_URL,
    get_nearby_hotspots,
)
from tests.unit import mixins


class GetNearbyHotspotsTests(
    TestCase,
    mixins.BackTestsMixin,
    mixins.DistTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.LatTestsMixin,
    mixins.LngTestsMixin,
):
    """Tests for the get_nearby_hotspots() API call."""

    def get_callable(self):
        return get_nearby_hotspots

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "lat": "45.0",
            "lng": "45.0",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(NEARBY_HOTSPOTS_URL, url)
