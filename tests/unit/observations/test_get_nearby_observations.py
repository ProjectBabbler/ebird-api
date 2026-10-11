from unittest import TestCase

from ebird.api.requests.observations import (
    NEARBY_OBSERVATIONS_URL,
    get_nearby_observations,
)
from tests.unit import mixins


class GetGeoObservationsTests(
    TestCase,
    mixins.BackTestsMixin,
    mixins.CategoryTestsMixin,
    mixins.DistTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.LatTestsMixin,
    mixins.LngTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.ProvisionalTestsMixin,
    mixins.SortTestsMixin,
    mixins.SpeciesLocaleTestsMixin,
):
    """Tests for the get_nearest_observations() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_nearby_observations

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
        self.assertEqual(NEARBY_OBSERVATIONS_URL, url)
