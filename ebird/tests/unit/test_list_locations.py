# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ebird.core import list_locations, LIST_LOCATIONS_URL


# noinspection PyUnusedLocal
def get_locations(url, params):
    pass


class ListLocationsTests(TestCase):
    """Tests for the list_locations() API call.

    Since the function only has 2 arguments (one positional, one
    keyword) the data patterns can be simplified if we treat the
    arguments as just being positional while still maintaining
    readability.

    """
    parameters = [
        (('bcr',  None), {'rtype': 'bcr'}),
        (('country',  None), {'rtype': 'country'}),
        (('subnational1', 'US'), {'rtype': 'subnational1', 'countryCode': 'US'}),
        (('subnational2', 'US'), {'rtype': 'subnational2', 'countryCode': 'US'}),
        (('subnational2', 'US-NV'), {'rtype': 'subnational2', 'subnational1Code': 'US-NV'}),
    ]

    validation = [
        ('bcr', 'US'),
        ('bcr', 'US-NV'),
        ('bcr', 'US-NV-001'),
        ('country', 'US'),
        ('country', 'US-NV'),
        ('country', 'US-NV-001'),
        ('subnational1', 'US-NV'),
        ('subnational1', 'US-NV-001'),
        ('subnational2', 'US-NV-001'),
        ('other', 'US'),
    ]

    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        list_locations('country')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(LIST_LOCATIONS_URL, actual)

    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            list_locations(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.core.get_locations', side_effect=get_locations)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                list_locations(*args)
