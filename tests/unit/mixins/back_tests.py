from ebird.api.requests.constants import DEFAULT_BACK
from tests.unit.mixins.base import BaseMixin


class BackTestsMixin(BaseMixin):
    def test_back_is_sent(self):
        query = self.api_call(back=10)[1]
        self.assertEqual(query["back"], 10)

    def test_default_back_is_not_sent(self):
        query = self.api_call(back=DEFAULT_BACK)[1]
        self.assertTrue("back" not in query)

    def test_invalid_back_raises_error(self):
        self.api_raises(ValueError, back=31)
        self.api_raises(ValueError, back="x")
