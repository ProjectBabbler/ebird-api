# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.observations import NOTABLE_OBSERVATIONS_URL, get_notable_observations

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.observations.get_content', side_effect=get_content)
class GetRegionObservationsTests(
    mixins.AreaTestsMixin,
    mixins.BackTestsMixin,
    mixins.DetailTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.LocaleTestsMixin,
    mixins.MaxObservationsTestsMixin,
    TestCase
):
    """Tests for the get_nearest_notable() API call."""

    def get_max_results_default(self):
        return None

    def get_fixture(self):
        return get_notable_observations

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'area': 'US-NV',
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(NOTABLE_OBSERVATIONS_URL % 'US-NV', actual)

    def test_request_for_multiple_areas_url(self, mocked_function):
        self.get_fixture()(**self.get_params(area='US-NV,US-WY,US-AZ'))
        actual = mocked_function.call_args[0][0]
        self.assertEqual(NOTABLE_OBSERVATIONS_URL % 'US-NV', actual)

    def test_request_for_multiple_areas_parameter(self, mocked_function):
        self.get_fixture()(**self.get_params(area='US-NV,US-WY,US-AZ'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['r'], 'US-NV,US-WY,US-AZ')