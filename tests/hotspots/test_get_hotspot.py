# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.hotspots import HOTSPOT_INFO_URL, get_hotspot

from tests.mixins import HeaderTestsMixin


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.hotspots.get_content', side_effect=get_content)
class GetHotspotTests(HeaderTestsMixin, TestCase):
    """Tests for the get_hotspot() API call."""

    def get_fixture(self):
        return get_hotspot

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'loc_id': 'L123456',
        }
        params.update(kwargs)
        return params

    def test_url_contains_location_code(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(HOTSPOT_INFO_URL % 'L123456', actual)

    def test_invalid_location_code_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(loc_id='123456'))
