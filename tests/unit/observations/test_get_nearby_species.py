from unittest import TestCase

from ebird.api.requests.observations import (
    NEARBY_SPECIES_URL,
    get_nearby_species,
)
from tests.unit import mixins


class GetGeoSpeciesTests(
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
    mixins.SpeciesLocaleTestsMixin,
):
    """Tests for the get_nearest_species() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_nearby_species

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
        url = self.api_call()[0]
        self.assertEqual(NEARBY_SPECIES_URL % self.get_params()["species"], url)
