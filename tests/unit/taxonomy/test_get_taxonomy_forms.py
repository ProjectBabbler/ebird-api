from unittest import TestCase
from unittest.mock import patch

from ebird.api.taxonomy import TAXONOMY_FORMS_URL, get_taxonomy_forms

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.taxonomy.get_content', side_effect=get_content)
class GetTaxonomyFormsTests(
        mixins.HeaderTestsMixin,
        TestCase):
    """Tests for the get_taxonomy_forms() API call."""

    def get_fixture(self):
        return get_taxonomy_forms

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'species': 'horlar',
        }
        params.update(kwargs)
        return params

    def test_url_contains_species_code(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TAXONOMY_FORMS_URL % 'horlar', actual)

    def test_invalid_species_code_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(species='abc'))

    def test_query_params_are_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][1]
        self.assertDictEqual({}, actual)
