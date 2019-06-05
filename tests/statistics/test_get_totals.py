# -*- coding: utf-8 -*-

from datetime import date

from unittest import TestCase
from unittest.mock import patch

from ebird.api.statistics import TOTALS_URL, get_totals

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.statistics.get_content', side_effect=get_content)
class GetTotalsTests(
    mixins.HeaderTestsMixin,
    TestCase
):
    """Tests for the get_totals() API call."""

    def get_fixture(self):
        return get_totals

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'area': 'US-NV',
            'date': date.today()
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        params = self.get_params()
        self.get_fixture()(**params)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TOTALS_URL % ('US-NV', params['date'].strftime('%Y/%m/%d')), actual)
