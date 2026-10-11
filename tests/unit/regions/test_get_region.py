from unittest import TestCase

from ebird.api.requests.regions import REGION_INFO_URL, get_region
from tests.unit.mixins import HeaderTestsMixin


class GetRegionTests(TestCase, HeaderTestsMixin):
    """Tests for the get_region() API call."""

    def get_callable(self):
        return get_region

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "region": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_code(self):
        url = self.api_call()[0]
        self.assertEqual(REGION_INFO_URL % "US-NV", url)

    def test_invalid_region_code_raises_error(self):
        self.api_raises(ValueError, region="aa-bb-cc-dd")
