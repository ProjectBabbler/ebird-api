from datetime import date
from unittest import TestCase

from ebird.api.requests.statistics import TOTALS_URL, get_totals
from tests.unit.mixins import HeaderTestsMixin


class GetTotalsTests(TestCase, HeaderTestsMixin):
    """Tests for the get_totals() API call."""

    def get_callable(self):
        return get_totals

    def get_params(self, **kwargs):
        params = {"token": "12345", "area": "US-NV", "date": date.today()}
        params.update(kwargs)
        return params

    def test_request_url(self):
        params = self.get_params()
        url = self.api_call()[0]
        self.assertEqual(
            TOTALS_URL % ("US-NV", params["date"].strftime("%Y/%m/%d")), url
        )
