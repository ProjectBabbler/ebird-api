# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.taxonomy import TAXONOMY_GROUPS_URL, get_taxonomy_groups

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.taxonomy.get_content', side_effect=get_content)
class GetTaxonomyGroupsTests(
        mixins.HeaderTestsMixin,
        mixins.GroupLocaleTestsMixin,
        TestCase):
    """Tests for the get_taxonomy_groups() API call."""

    def get_fixture(self):
        return get_taxonomy_groups

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
        }
        params.update(kwargs)
        return params

    def test_url_contains_grouping(self, mocked_function):
        self.get_fixture()(**self.get_params(ordering='merlin'))
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TAXONOMY_GROUPS_URL % 'merlin', actual)

    def test_url_contains_default_grouping(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TAXONOMY_GROUPS_URL % 'ebird', actual)

    def test_invalid_grouping_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(ordering='other'))
