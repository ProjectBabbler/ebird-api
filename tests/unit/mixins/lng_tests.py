from tests.unit.mixins.base import BaseMixin


class LngTestsMixin(BaseMixin):
    def test_lng_is_sent(self):
        query = self.api_call(lng="90.0")[1]
        self.assertEqual(query["lng"], "90.00")

    def test_invalid_lng_raises_error(self):
        self.api_raises(ValueError, lng="180.1")
        self.api_raises(ValueError, lng="-180.1")
        self.api_raises(ValueError, lng="x")
