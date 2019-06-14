# -*- coding: utf-8 -*-

from datetime import date

from unittest import TestCase
from unittest.mock import patch

from ebird.api.checklists import CHECKLISTS_RECENT_URL, CHECKLISTS_DATE_URL, get_visits

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.checklists.get_content', side_effect=get_content)
class GetVisitsTests(
    mixins.HeaderTestsMixin,
    mixins.MaxChecklistsTestsMixin,
    TestCase
):
    """Tests for the get_visits() API call."""

    def get_fixture(self):
        return get_visits

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'area': 'US-NV',
        }
        params.update(kwargs)
        return params

    def test_recent_visits_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(CHECKLISTS_RECENT_URL % 'US-NV', actual)

    def test_visits_on_date_url(self, mocked_function):
        params = self.get_params(date=date.today())
        self.get_fixture()(**params)
        expected = CHECKLISTS_DATE_URL % ('US-NV', params['date'].strftime('%Y/%m/%d'))
        actual = mocked_function.call_args[0][0]
        self.assertEqual(expected, actual)
