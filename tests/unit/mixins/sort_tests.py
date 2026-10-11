from ebird.api.requests.constants import DEFAULT_OBSERVATION_ORDER
from tests.unit.mixins.base import BaseMixin


class SortTestsMixin(BaseMixin):
    def test_sort_is_sent(self):
        query = self.api_call(sort="species")[1]
        self.assertEqual(query["sort"], "species")

    def test_default_sort_is_not_sent(self):
        query = self.api_call(sort=DEFAULT_OBSERVATION_ORDER)[1]
        self.assertTrue("sort" not in query)

    def test_invalid_sort_raises_error(self):
        self.api_raises(ValueError, sort="none")
