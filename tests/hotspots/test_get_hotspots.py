# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.hotspots import REGION_HOTSPOTS_URL, get_hotspots

from tests.mixins import BackTestsMixin, HeaderTestsMixin


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.hotspots.get_content', side_effect=get_content)
class GetHotspotsTests(
        BackTestsMixin,
        HeaderTestsMixin,
        TestCase):
    """Tests for the get_hotspots() API call."""

    def get_fixture(self):
        return get_hotspots

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
        self.assertEqual(REGION_HOTSPOTS_URL % 'US-NV', actual)
