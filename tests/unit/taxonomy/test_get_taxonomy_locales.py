from unittest import TestCase

from ebird.api.requests.taxonomy import (
    TAXONOMY_LOCALES_URL,
    get_taxonomy_locales,
)
from tests.unit.mixins import HeaderTestsMixin


class GetTaxonomyLocalesTests(TestCase, HeaderTestsMixin):
    """Tests for the get_taxonomy_locales() API call."""

    def get_callable(self):
        return get_taxonomy_locales

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(TAXONOMY_LOCALES_URL, url)

    def test_query_params_are_not_sent(self):
        query = self.api_call()[1]
        self.assertDictEqual({}, query)
