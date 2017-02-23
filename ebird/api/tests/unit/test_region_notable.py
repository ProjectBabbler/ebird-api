# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.data import REGION_NOTABLE_URL, region_notable


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class RegionNotableTests(TestCase):

    parameters = [
        (  # Only the format is added when default arguments are used
            (('US-NV',), {}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Default back is filtered out
            (('US-NV',), {'back': 14}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for back is filtered out
            (('US-NV',), {'back': 10}),
            {'r': 'US-NV', 'back': 10, 'fmt': 'json'}),
        (  # Default max_results is filtered out
            (('US-NV',), {'max_results': None}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for max_results is included
            (('US-NV',), {'max_results': 10}),
            {'r': 'US-NV', 'maxResults': 10, 'fmt': 'json'}),
        (  # Default locale is filtered out
            (('US-NV',), {'locale': 'en_US'}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for locale is included
            (('US-NV',), {'locale': 'de_DE'}),
            {'r': 'US-NV', 'locale': 'de_DE', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            (('US-NV',), {'hotspot': False}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for hotspot is included
            (('US-NV',), {'hotspot': True}),
            {'r': 'US-NV', 'hotspot': 'true', 'fmt': 'json'}),
        (  # Default detail is filtered out
            (('US-NV',), {'detail': 'simple'}),
            {'r': 'US-NV', 'fmt': 'json'}),
        (  # Value for detail is included
            (('US-NV',), {'detail': 'full'}),
            {'r': 'US-NV', 'detail': 'full', 'fmt': 'json'}),
    ]

    validation = [
        (('U',), {}),  # region code is invalid
        (('',), {}),  # region code is blank
        (('US-NV',), {'back': 31}),  # back is more than 30
        (('US-NV',), {'back': 0}),  # back is less than 1
        (('US-NV',), {'back': 'str'}),  # back cannot be converted to an integer
        (('US-NV',), {'max_results': 10001}),  # max_results is more than 10000
        (('US-NV',), {'max_results': 0}),  # max_results is less than 1
        (('US-NV',), {'max_results': 'str'}),  # max_results is not an integer
        (('US-NV',), {'locale': 'enUS'}),  # locale is not valid
        (('US-NV',), {'locale': ''}),  # locale is blank
        # TODO add validation pattern for hotspot
        (('US-NV',), {'detail': 'complex'}),  # detail is not a recognised value
        (('US-NV',), {'detail': ''}),  # detail is blank
    ]

    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        region_notable('US-NV')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(REGION_NOTABLE_URL, actual)

    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, ((args, kwargs), expected) in enumerate(self.parameters):
            region_notable(*args, **kwargs)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, (args, kwargs) in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                region_notable(*args, **kwargs)
