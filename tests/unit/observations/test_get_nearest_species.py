# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.observations import NEAREST_SPECIES_URL, get_nearest_species

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.observations.get_content', side_effect=get_content)
class GetNearestSpeciesTests(
    mixins.BackTestsMixin,
    mixins.DistTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.LatTestsMixin,
    mixins.LngTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.ProvisionalTestsMixin,
    TestCase
):
    """Tests for the get_nearest_species() API call."""

    def get_max_results_default(self):
        return None

    def get_fixture(self):
        return get_nearest_species

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'species': 'horlar',
            'lat': '45.0',
            'lng': '45.0',
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        params = self.get_params()
        self.get_fixture()(**params)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(NEAREST_SPECIES_URL % params['species'], actual)
