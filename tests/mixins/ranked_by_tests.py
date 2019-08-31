from ebird.api.constants import DEFAULT_TOP_100_RANK
from tests.mixins import BaseMixin


class RankedByTestsMixin(BaseMixin):

    def test_rank_by_checklists_is_sent(self):
        query = self.api_call(rank='cl')[1]
        self.assertEqual(query['rankedBy'], 'cl')

    def test_default_rank_by_species_is_not_sent(self):
        query = self.api_call(rank=DEFAULT_TOP_100_RANK)[1]
        self.assertTrue('rankedBy' not in query)
