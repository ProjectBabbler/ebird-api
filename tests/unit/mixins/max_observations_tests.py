from ebird.api.requests.constants import DEFAULT_MAX_OBSERVATIONS
from tests.unit.mixins.base import BaseMixin


class MaxObservationsTestsMixin(BaseMixin):
    def test_max_results_is_sent(self):
        query = self.api_call(max_results=1)[1]
        self.assertEqual(query["maxResults"], 1)

    def test_default_max_results_is_not_sent(self):
        query = self.api_call(max_results=DEFAULT_MAX_OBSERVATIONS)[1]
        self.assertTrue("maxResults" not in query)

    def test_invalid_max_results_raises_error(self):
        self.api_raises(ValueError, max_results=0)
        self.api_raises(ValueError, max_results=10001)
