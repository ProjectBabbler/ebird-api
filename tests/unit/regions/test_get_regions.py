# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.regions import REGION_LIST_URL, get_regions

from tests.mixins import HeaderTestsMixin


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.regions.get_content', side_effect=get_content)
class GetRegionsTests(HeaderTestsMixin, TestCase):
    """Tests for the get_regions() API call."""

    def get_fixture(self):
        return get_regions

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'rtype': 'subnational2',
            'region': 'US-NV',
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_type_and_code(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(REGION_LIST_URL % ('subnational2', 'US-NV'), actual)

    def test_invalid_region_type_raises_error(self, mocked_function):  # noqa
        params = self.get_params(rtype='county', region='US')
        self.assertRaises(ValueError, self.get_fixture(), **params)

    def test_invalid_region_code_raises_error(self, mocked_function):  # noqa
        params = self.get_params(rtype='country', region='aa-bb-cc-dd')
        self.assertRaises(ValueError, self.get_fixture(), **params)
