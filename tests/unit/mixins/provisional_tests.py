from ebird.api.requests.constants import DEFAULT_PROVISIONAL
from tests.unit.mixins.base import BaseMixin


class ProvisionalTestsMixin(BaseMixin):
    def test_include_provisional_is_sent(self):
        query = self.api_call(provisional=True)[1]
        self.assertEqual(query["includeProvisional"], "true")

    def test_default_include_provisional_is_not_sent(self):
        query = self.api_call(provisional=DEFAULT_PROVISIONAL == "true")[1]
        self.assertTrue("includeProvisional" not in query)
