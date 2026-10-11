from ebird.api.requests.constants import DEFAULT_DETAIL
from tests.unit.mixins.base import BaseMixin


class DetailTestsMixin(BaseMixin):
    def test_detail_is_sent(self):
        query = self.api_call(detail="full")[1]
        self.assertEqual(query["detail"], "full")

    def test_default_detail_is_not_sent(self):
        query = self.api_call(detail=DEFAULT_DETAIL)[1]
        self.assertTrue("detail" not in query)

    def test_invalid_detail_raises_error(self):
        self.api_raises(ValueError, detail="empty")
