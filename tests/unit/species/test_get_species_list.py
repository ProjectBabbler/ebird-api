from unittest import TestCase

from ebird.api.requests.species import SPECIES_LIST_URL, get_species_list
from tests.unit.mixins import HeaderTestsMixin


class GetSpeciesListTests(TestCase, HeaderTestsMixin):
    """Tests for the get_species_list() API call."""

    def get_callable(self):
        return get_species_list

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "area": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_code(self):
        url = self.api_call()[0]
        self.assertEqual(SPECIES_LIST_URL % "US-NV", url)

    def test_invalid_region_code_raises_error(self):
        self.api_raises(ValueError, area="aa-bb-cc-dd")
