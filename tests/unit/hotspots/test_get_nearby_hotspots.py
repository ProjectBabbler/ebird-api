# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.hotspots import NEARBY_HOTSPOTS_URL, get_nearby_hotspots

from tests.mixins import (
    LatTestsMixin, LngTestsMixin, DistTestsMixin, BackTestsMixin, HeaderTestsMixin)


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.hotspots.get_content', side_effect=get_content)
class GetNearbyHotspotsTests(
        BackTestsMixin,
        DistTestsMixin,
        HeaderTestsMixin,
        LatTestsMixin,
        LngTestsMixin,
        TestCase):
    """Tests for the get_nearby_hotspots() API call."""

    def get_fixture(self):
        return get_nearby_hotspots

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'lat': '45.0',
            'lng': '45.0',
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(NEARBY_HOTSPOTS_URL, actual)
