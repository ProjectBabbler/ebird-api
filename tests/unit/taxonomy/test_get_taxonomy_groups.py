from unittest import TestCase

from ebird.api.requests.taxonomy import (
    TAXONOMY_GROUPS_URL,
    get_taxonomy_groups,
)
from tests.unit.mixins import GroupLocaleTestsMixin, HeaderTestsMixin


class GetTaxonomyGroupsTests(TestCase, HeaderTestsMixin, GroupLocaleTestsMixin):
    """Tests for the get_taxonomy_groups() API call."""

    def get_callable(self):
        return get_taxonomy_groups

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
        }
        params.update(kwargs)
        return params

    def test_url_contains_grouping(self):
        url = self.api_call(ordering="merlin")[0]
        self.assertEqual(TAXONOMY_GROUPS_URL % "merlin", url)

    def test_url_contains_default_grouping(self):
        url = self.api_call()[0]
        self.assertEqual(TAXONOMY_GROUPS_URL % "ebird", url)

    def test_invalid_grouping_raises_error(self):
        self.api_raises(ValueError, ordering="other")
