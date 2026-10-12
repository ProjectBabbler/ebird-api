from datetime import date
from unittest import TestCase

from ebird.api.requests.statistics import TOP_100_URL, get_top_100
from tests.unit.mixins import (
    HeaderTestsMixin,
    MaxObserversTestsMixin,
    RankedByTestsMixin,
)


class GetTop100Tests(
    TestCase, HeaderTestsMixin, RankedByTestsMixin, MaxObserversTestsMixin
):
    """Tests for the get_top_100() API call."""

    def get_callable(self):
        return get_top_100

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "region": "US-NV",
            "date": date.today(),
            "rank": "spp",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        params = self.get_params()
        url = self.api_call()[0]
        self.assertEqual(
            TOP_100_URL % ("US-NV", params["date"].strftime("%Y/%m/%d")), url
        )

    def test_location(self):
        params = self.get_params(region="L99381")
        url = self.api_call(region="L99381")[0]
        self.assertEqual(
            TOP_100_URL % ("L99381", params["date"].strftime("%Y/%m/%d")), url
        )

    def test_country(self):
        params = self.get_params(region="us")
        url = self.api_call(region="us")[0]
        self.assertEqual(TOP_100_URL % ("US", params["date"].strftime("%Y/%m/%d")), url)

    def test_subnational2_is_invalid(self):
        self.api_raises(ValueError, region="US-NV-11")

    def test_invalid_region(self):
        self.api_raises(ValueError, region="invalid")
