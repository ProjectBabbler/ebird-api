from unittest import TestCase

from ebird.api.requests.observations import (
    NEARBY_NOTABLE_URL,
    get_nearby_notable,
)
from tests.unit import mixins


class GetGeoNotableTests(
    TestCase,
    mixins.BackTestsMixin,
    mixins.DetailTestsMixin,
    mixins.DistTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.LatTestsMixin,
    mixins.LngTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.SpeciesLocaleTestsMixin,
):
    """Tests for the get_nearest_notable() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_nearby_notable

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
        self.assertEqual(NEARBY_NOTABLE_URL, url)
