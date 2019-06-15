# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.regions import REGION_INFO_URL, get_region

from tests.mixins import HeaderTestsMixin


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.regions.get_content', side_effect=get_content)
class GetRegionTests(HeaderTestsMixin, TestCase):
    """Tests for the get_region() API call."""

    def get_fixture(self):
        return get_region

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'region': 'US-NV',
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_code(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(REGION_INFO_URL % 'US-NV', actual)

    def test_invalid_region_code_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(region='aa-bb-cc-dd'))
