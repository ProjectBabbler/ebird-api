# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ebird.data import REGION_SPECIES_URL, region_species


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class RegionSpeciesTests(TestCase):

    parameters = [
        (  # Only the format is added when default arguments are used
            (('Apus apus', 'US-NV',), {}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Default back is filtered out
            (('Apus apus', 'US-NV',), {'back': 14}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for back is filtered out
            (('Apus apus', 'US-NV',), {'back': 10}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'back': 10, 'fmt': 'json'}),
        (  # Default max_results is filtered out
            (('Apus apus', 'US-NV',), {'max_results': None}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for max_results is included
            (('Apus apus', 'US-NV',), {'max_results': 10}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'maxResults': 10, 'fmt': 'json'}),
        (  # Default locale is filtered out
            (('Apus apus', 'US-NV',), {'locale': 'en_US'}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for locale is included
            (('Apus apus', 'US-NV',), {'locale': 'de_DE'}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'locale': 'de_DE', 'fmt': 'json'}),
        (  # Default provisional is filtered out
            (('Apus apus', 'US-NV',), {'provisional': False}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for provisional is included
            (('Apus apus', 'US-NV',), {'provisional': True}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'includeProvisional': 'true', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            (('Apus apus', 'US-NV',), {'hotspot': False}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for hotspot is included
            (('Apus apus', 'US-NV',), {'hotspot': True}),
            {'sci': 'Apus apus', 'r': 'US-NV', 'hotspot': 'true', 'fmt': 'json'}),
    ]

    validation = [
        (('', 'L',), {}),  # species name is blank
        (('Apus apus', 'L',), {}),  # location code is invalid
        (('Apus apus', '',), {}),  # location code is blank
        (('Apus apus', 'US-NV',), {'back': 31}),  # back is more than 30
        (('Apus apus', 'US-NV',), {'back': 0}),  # back is less than 1
        (('Apus apus', 'US-NV',), {'back': 'str'}),  # back cannot be converted to an integer
        (('Apus apus', 'US-NV',), {'max_results': 10001}),  # max_results is more than 10000
        (('Apus apus', 'US-NV',), {'max_results': 0}),  # max_results is less than 1
        (('Apus apus', 'US-NV',), {'max_results': 'str'}),  # max_results is not an integer
        (('Apus apus', 'US-NV',), {'locale': 'enUS'}),  # locale is not valid
        (('Apus apus', 'US-NV',), {'locale': ''}),  # locale is blank
        # TODO Currently do not have validation tests for provisional
        # TODO Currently do not have validation tests for hotspot
    ]

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        region_species('Apus apus', 'US-NV')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(REGION_SPECIES_URL, actual)

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, ((args, kwargs), expected) in enumerate(self.parameters):
            region_species(*args, **kwargs)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, (args, kwargs) in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                region_species(*args, **kwargs)
