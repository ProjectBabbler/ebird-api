from unittest import TestCase

from ebird.api.requests.taxonomy import (
    TAXONOMY_VERSIONS_URL,
    get_taxonomy_versions,
)
from tests.unit.mixins import HeaderTestsMixin


class GetTaxonomyVersionsTests(TestCase, HeaderTestsMixin):
    """Tests for the get_taxonomy_versions() API call."""

    def get_callable(self):
        return get_taxonomy_versions

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(TAXONOMY_VERSIONS_URL, url)

    def test_query_params_are_not_sent(self):
        query = self.api_call()[1]
        self.assertDictEqual({}, query)
