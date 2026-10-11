from ebird.api.requests.constants import DEFAULT_HOTSPOTS_ONLY
from tests.unit.mixins.base import BaseMixin


class HotspotTestsMixin(BaseMixin):
    def test_hotspot_is_sent(self):
        query = self.api_call(hotspot=True)[1]
        self.assertEqual(query["hotspot"], "true")

    def test_default_hotspot_is_not_sent(self):
        query = self.api_call(hotspot=DEFAULT_HOTSPOTS_ONLY == "true")[1]
        self.assertTrue("hotspot" not in query)
