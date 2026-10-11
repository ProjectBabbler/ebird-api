from ebird.api.requests.constants import DEFAULT_DISTANCE
from tests.unit.mixins.base import BaseMixin


class DistTestsMixin(BaseMixin):
    def test_dist_is_sent(self):
        query = self.api_call(dist=50)[1]
        self.assertEqual(query["dist"], 50)

    def test_default_dist_is_not_sent(self):
        query = self.api_call(dist=DEFAULT_DISTANCE)[1]
        self.assertTrue("dist" not in query)

    def test_invalid_dist_raises_error(self):
        self.api_raises(ValueError, dist=51)
        self.api_raises(ValueError, dist="x")
