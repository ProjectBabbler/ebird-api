# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.reference import LIST_REGIONS_URL, list_regions


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class ListRegionsTests(TestCase):
    """Tests for the list_regions() API call.

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

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        list_regions('country')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(LIST_REGIONS_URL, actual)

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            list_regions(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                list_regions(*args)
