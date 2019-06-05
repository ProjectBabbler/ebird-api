# -*- coding: utf-8 -*-

from unittest import TestCase, skip
from unittest.mock import patch

from ebird.api.taxonomy import TAXONOMY_URL, get_taxonomy

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.taxonomy.get_content', side_effect=get_content)
class GetTaxonomyTests(
        mixins.HeaderTestsMixin,
        mixins.LocaleTestsMixin,
        TestCase):
    """Tests for the get_taxonomy() API call."""

    def get_fixture(self):
        return get_taxonomy

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TAXONOMY_URL, actual)

    def test_requested_format_is_json(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['fmt'], 'json')

    def test_species_category_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['cat'], 'species')

    def test_default_species_category_is_excluded(self, mocked_function):
        self.get_fixture()(**self.get_params(category=None))
        actual = mocked_function.call_args[0][1]
        self.assertFalse('cat' in actual)

    def test_multiple_species_categories(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species,domestic'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['cat'], 'species,domestic')

    def test_invalid_species_category_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(category='abc'))

    def test_version_is_not_sent_by_default(self, mocked_function):  # noqa
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][1]
        self.assertFalse('version' in actual)

    def test_version_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(version='2017.1'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['version'], '2017.1')

    def test_species_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species', species='horlar'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['species'], 'horlar')

    def test_species_accepts_list(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species', species=['horlar', 'crelar']))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['species'], 'horlar,crelar')

    def test_species_whitespace_in_string_is_stripped(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species', species=' horlar , crelar '))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['species'], 'horlar,crelar')

    def test_species_whitespace_in_list_is_stripped(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species', species=['horlar ', ' crelar']))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['species'], 'horlar,crelar')

    def test_species_must_be_string_or_list(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(category='species', species={}))

    def test_species_in_list_cannot_be_blank(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(category='species', species='horlar,'))
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(category='species', species=['horlar', '']))

#    def test_using_category_and_species_raises_error(self, mocked_function):  # noqa
#        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(species='horlar'))
