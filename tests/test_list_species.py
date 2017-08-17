# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.reference import LIST_SPECIES_URL, list_species


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class ListSpeciesTests(TestCase):
    """Tests for the list_species() API call.

    Since the function only has 2 (keyword) arguments the data patterns
    can be simplified if we treat the arguments as just being positional
    while still maintaining readability.

    """
    parameters = [
        (('species',), {}),
        (('domestic',), {'cat': 'domestic'}),
        (('domestic,spuh',), {'cat': 'domestic,spuh'}),
        (('species', 'en_US'), {}),
        (('species', 'es'), {'locale': 'es'}),
    ]

    validation = [
        # Species category is blank
        ('',),
        # Species category is invalid
        ('other',),
        # Species category contains invalid value
        ('species,other,spuh',),
        # locale is invalid
        ('species', 'enUS')
    ]

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        list_species()
        actual = mocked_function.call_args[0][0]
        self.assertEqual(LIST_SPECIES_URL, actual)

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            list_species(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                list_species(*args)
