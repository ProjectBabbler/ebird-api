from unittest import TestCase

from ebird.api.requests.regions import REGION_LIST_URL, get_regions
from tests.unit.mixins import HeaderTestsMixin


class GetRegionsTests(TestCase, HeaderTestsMixin):
    """Tests for the get_regions() API call."""

    def get_callable(self):
        return get_regions

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "rtype": "subnational2",
            "region": "US-NV",
        }
        params.update(kwargs)
        return params

    def test_url_contains_region_type_and_code(self):
        url = self.api_call()[0]
        self.assertEqual(REGION_LIST_URL % ("subnational2", "US-NV"), url)

    def test_invalid_region_type_raises_error(self):
        self.api_raises(ValueError, rtype="county", region="US")

    def test_invalid_region_code_raises_error(self):
        self.api_raises(ValueError, rtype="country", region="aa-bb-cc-dd")
