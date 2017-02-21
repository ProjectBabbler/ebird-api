# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ebird.data import GEO_SPECIES_URL, geo_species


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class NearestSpeciesTests(TestCase):

    parameters = [
        (  # Only the format is added when default arguments are used
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Default back is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'back': 14},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for back is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'back': 10},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'back': 10, 'fmt': 'json'}),
        (  # Default max_results is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'max_results': None},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for max_results is included
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'max_results': 10},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'maxResults': 10, 'fmt': 'json'}),
        (  # Default locale is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'locale': 'en_US'},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for locale is included
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'locale': 'de_DE'},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'locale': 'de_DE', 'fmt': 'json'}),
        (  # Default provisional is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'provisional': False},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for provisional is included
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'provisional': True},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'includeProvisional': 'true', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'hotspot': False},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for hotspot is included
            {'species': 'Apus apus', 'lat': 1.0, 'lng': 0.0, 'hotspot': True},
            {'sci': 'Apus apus', 'lat': '1.00', 'lng': '0.00', 'hotspot': 'true', 'fmt': 'json'}),
    ]

    validation = [
        {'species': 'Apus apus', 'lat': 91, 'lng': 0.0},  # lat is more than 90
        {'species': 'Apus apus', 'lat': -91, 'lng': 0.0},  # lat is less than 90
        {'species': 'Apus apus', 'lat': 'str', 'lng': 0.0},  # lat cannot be converted to a float
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 181},  # lat is more than 90
        {'species': 'Apus apus', 'lat': 0.0, 'lng': -181},  # lat is less than 90
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 'str'},  # lat cannot be converted to a float
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'back': 31},  # back is more than 30
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'back': 0},  # back is less than 1
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'back': 'str'},  # back cannot be converted to an integer
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'max_results': 10001},  # max_results is more than 10000
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'max_results': 0},  # max_results is less than 1
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'max_results': 'str'},  # max_results is not an integer
        {'species': 'Apus apus', 'lat': 0.0, 'lng': 0.0, 'locale': 'enUS'},  # locale is not valid
        # TODO Currently do not have validation tests for provisional
        # TODO Currently do not have validation tests for hotspot
    ]

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        geo_species('Apus apus', 0.0, 0.0)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(GEO_SPECIES_URL, actual)

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (pattern, expected) in enumerate(self.parameters):
            geo_species(**pattern)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, pattern in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                geo_species(**pattern)
