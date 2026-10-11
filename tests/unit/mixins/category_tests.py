from ebird.api.requests.constants import DEFAULT_SPECIES_CATEGORY
from tests.unit.mixins.base import BaseMixin


class CategoryTestsMixin(BaseMixin):
    def test_category_is_sent(self):
        query = self.api_call(category="species")[1]
        self.assertEqual(query["cat"], "species")

    def test_default_category_is_not_sent(self):
        query = self.api_call(category=DEFAULT_SPECIES_CATEGORY)[1]
        self.assertTrue("cat" not in query)

    def test_invalid_category_raises_error(self):
        self.api_raises(ValueError, category="none")
