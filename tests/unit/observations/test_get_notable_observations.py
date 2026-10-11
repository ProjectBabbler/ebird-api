from unittest import TestCase

from ebird.api.requests.observations import (
    NOTABLE_OBSERVATIONS_URL,
    get_notable_observations,
)
from tests.unit import mixins


class GetRegionObservationsTests(
    TestCase,
    mixins.AreaTestsMixin,
    mixins.BackTestsMixin,
    mixins.DetailTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.SpeciesLocaleTestsMixin,
):
    """Tests for the get_nearest_notable() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_notable_observations

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "area": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(NOTABLE_OBSERVATIONS_URL % "US-NV", url)

    def test_request_for_multiple_areas_url(self):
        url = self.api_call(area="US-NV,US-WY,US-AZ")[0]
        self.assertEqual(NOTABLE_OBSERVATIONS_URL % "US-NV", url)

    def test_request_for_multiple_areas_parameter(self):
        query = self.api_call(area="US-NV,US-WY,US-AZ")[1]
        self.assertEqual(query["r"], "US-NV,US-WY,US-AZ")
