from unittest import TestCase

from ebird.api.requests.observations import (
    NEAREST_SPECIES_URL,
    get_nearest_species,
)
from tests.unit import mixins


class GetNearestSpeciesTests(
    TestCase,
    mixins.BackTestsMixin,
    mixins.DistTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.LatTestsMixin,
    mixins.LngTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.ProvisionalTestsMixin,
):
    """Tests for the get_nearest_species() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_nearest_species

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "species": "horlar",
            "lat": "45.0",
            "lng": "45.0",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        params = self.get_params()
        url = self.api_call()[0]
        self.assertEqual(NEAREST_SPECIES_URL % params["species"], url)
