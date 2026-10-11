from ebird.api.requests.constants import DEFAULT_TAXONOMY_ORDER
from tests.unit.mixins.base import BaseMixin


class OrderingTestsMixin(BaseMixin):
    def test_ordering_is_sent(self):
        query = self.api_call(ordering="merlin")[1]
        self.assertEqual(query["speciesGrouping"], "species")

    def test_default_ordering_is_not_sent(self):
        query = self.api_call(ordering=DEFAULT_TAXONOMY_ORDER)[1]
        self.assertTrue("speciesGrouping" not in query)

    def test_invalid_ordering_raises_error(self):
        self.api_raises(ValueError, ordering="none")
