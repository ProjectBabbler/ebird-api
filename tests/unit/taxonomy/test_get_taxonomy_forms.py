from unittest import TestCase

from ebird.api.requests.taxonomy import TAXONOMY_FORMS_URL, get_taxonomy_forms
from tests.unit.mixins import HeaderTestsMixin


class GetTaxonomyFormsTests(TestCase, HeaderTestsMixin):
    """Tests for the get_taxonomy_forms() API call."""

    def get_callable(self):
        return get_taxonomy_forms

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "species": "horlar",
        }
        params.update(kwargs)
        return params

    def test_url_contains_species_code(self):
        url = self.api_call()[0]
        self.assertEqual(TAXONOMY_FORMS_URL % "horlar", url)

    def test_invalid_species_code_raises_error(self):
        self.api_raises(ValueError, species="abc")

    def test_query_params_are_not_sent(self):
        query = self.api_call()[1]
        self.assertDictEqual({}, query)
