# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.reference import LIST_HOTSPOTS_URL, list_hotspots


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class ListHotspotsTests(TestCase):
    """Tests for the list_hotspots() API call.

    Since the function only has 2 arguments (one positional, one
    keyword) the data patterns can be simplified if we treat the
    arguments as just being positional while still maintaining
    readability.

    """
    parameters = [
        (('US',  None), {'r': 'US',}),
        (('US',  1), {'r': 'US', 'back': 1}),
        (('US-NV', None), {'r': 'US-NV'}),
        (('US-NV', 1), {'r': 'US-NV', 'back': 1}),
        (('US-NV-001', None), {'r': 'US-NV-001'}),
        (('US-NV-001', 1), {'r': 'US-NV-001', 'back': 1}),
    ]

    validation = [
        # Region code is blank
        ('', None),
        # Region code is invalid
        ('other', None),
        # Back is less than 1
        ('US', 0),
        # Back is greater than 30
        ('US', 31),
    ]

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        list_hotspots('US', None)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(LIST_HOTSPOTS_URL, actual)

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            list_hotspots(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                list_hotspots(*args)
