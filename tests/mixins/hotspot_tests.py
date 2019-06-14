from ebird.api.constants import DEFAULT_HOTSPOTS_ONLY
from tests.mixins import BaseMixin


class HotspotTestsMixin(BaseMixin):

    def test_hotspot_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(hotspot=True))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['hotspot'], 'true')  # noqa

    def test_default_hotspot_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(hotspot=DEFAULT_HOTSPOTS_ONLY == 'true'))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('hotspot' not in actual)  # noqa
