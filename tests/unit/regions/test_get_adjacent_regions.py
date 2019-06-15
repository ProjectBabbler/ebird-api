# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.regions import ADJACENT_REGIONS_URL, get_adjacent_regions

from tests.mixins import HeaderTestsMixin


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.regions.get_content', side_effect=get_content)
class GetAdjacentRegionTests(HeaderTestsMixin, TestCase):
    """Tests for the get_adjacent_regions() API call."""

    def get_fixture(self):
        return get_adjacent_regions

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'region': 'US-NV',
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(ADJACENT_REGIONS_URL % 'US-NV', actual)
