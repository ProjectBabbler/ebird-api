# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ebird.core import find_locations, FIND_LOCATIONS_URL


# noinspection PyUnusedLocal
def get_locations(url, params):
    pass


class FindLocationsTests(TestCase):
    """Tests for the find_locations() API call."""

    parameters = [
        (('bcr',  'Coastal'), {'rtype': 'bcr', 'match': 'Coastal'}),
        (('country',  'North'), {'rtype': 'country', 'match': 'North'}),
        (('subnational1', 'South'), {'rtype': 'subnational1', 'match': 'South'}),
        (('subnational2', 'East'), {'rtype': 'subnational2', 'match': 'East'}),
    ]

    validation = [
        ('bcr', ''),
        ('other', 'west'),
    ]

    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        find_locations('country', 'North')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(FIND_LOCATIONS_URL, actual)

    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            find_locations(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                find_locations(*args)
