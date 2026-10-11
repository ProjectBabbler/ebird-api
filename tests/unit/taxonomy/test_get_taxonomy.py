from unittest import TestCase

from ebird.api.requests.taxonomy import TAXONOMY_URL, get_taxonomy
from tests.unit.mixins import HeaderTestsMixin, LocaleTestsMixin


class GetTaxonomyTests(TestCase, HeaderTestsMixin, LocaleTestsMixin):
    """Tests for the get_taxonomy() API call."""

    def get_callable(self):
        return get_taxonomy

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(TAXONOMY_URL, url)

    def test_requested_format_is_json(self):
        query = self.api_call()[1]
        self.assertEqual(query["fmt"], "json")

    def test_species_category_is_sent(self):
        query = self.api_call(category="species")[1]
        self.assertEqual(query["cat"], "species")

    def test_default_species_category_is_excluded(self):
        query = self.api_call(category=None)[1]
        self.assertFalse("cat" in query)

    def test_multiple_species_categories(self):
        query = self.api_call(category="species,domestic")[1]
        self.assertEqual(query["cat"], "species,domestic")

    def test_invalid_species_category_raises_error(self):
        self.api_raises(ValueError, category="abc")

    def test_version_is_not_sent_by_default(self):
        query = self.api_call()[1]
        self.assertFalse("version" in query)

    def test_version_is_sent(self):
        query = self.api_call(version="2017.1")[1]
        self.assertEqual(query["version"], "2017.1")

    def test_species_is_sent(self):
        query = self.api_call(category="species", species="horlar")[1]
        self.assertEqual(query["species"], "horlar")

    def test_species_accepts_list(self):
        query = self.api_call(category="species", species=["horlar", "crelar"])[1]
        self.assertEqual(query["species"], "horlar,crelar")

    def test_species_whitespace_in_string_is_stripped(self):
        query = self.api_call(category="species", species=" horlar , crelar ")[1]
        self.assertEqual(query["species"], "horlar,crelar")

    def test_species_whitespace_in_list_is_stripped(self):
        query = self.api_call(category="species", species=["horlar ", " crelar"])[1]
        self.assertEqual(query["species"], "horlar,crelar")

    def test_species_must_be_string_or_list(self):
        self.api_raises(ValueError, category="species", species={})

    def test_species_in_list_cannot_be_blank(self):
        self.api_raises(ValueError, category="species", species="horlar,")
        self.api_raises(ValueError, category="species", species=["horlar", ""])


#    def test_using_category_and_species_raises_error(self):
#        self.api_raises(ValueError, species='horlar')
