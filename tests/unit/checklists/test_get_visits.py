from datetime import date
from unittest import TestCase

from ebird.api.requests.checklists import (
    CHECKLISTS_DATE_URL,
    CHECKLISTS_RECENT_URL,
    get_visits,
)
from tests.unit.mixins import HeaderTestsMixin, MaxChecklistsTestsMixin


class GetVisitsTests(TestCase, HeaderTestsMixin, MaxChecklistsTestsMixin):
    """Tests for the get_visits() API call."""

    def get_callable(self):
        return get_visits

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "area": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_recent_visits_url(self):
        url = self.api_call()[0]
        self.assertEqual(CHECKLISTS_RECENT_URL % "US-NV", url)

    def test_visits_on_date_url(self):
        params = self.get_params(date=date.today())
        url = self.api_call(date=date.today())[0]
        expected = CHECKLISTS_DATE_URL % ("US-NV", params["date"].strftime("%Y/%m/%d"))
        self.assertEqual(expected, url)
