# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.data import HOTSPOT_OBSERVATIONS_URL, hotspot_observations


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class HotspotObservationsTests(TestCase):

    parameters = [
        (  # Only the format is added when default arguments are used
            (['L12345',], {}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Default back is filtered out
            (['L12345',], {'back': 14}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Value for back is filtered out
            (['L12345',], {'back': 10}),
            {'r': ['L12345',], 'back': 10, 'fmt': 'json'}),
        (  # Default max_results is filtered out
            (['L12345',], {'max_results': None}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Value for max_results is included
            (['L12345',], {'max_results': 10}),
            {'r': ['L12345',], 'maxResults': 10, 'fmt': 'json'}),
        (  # Default locale is filtered out
            (['L12345',], {'locale': 'en_US'}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Value for locale is included
            (['L12345',], {'locale': 'de_DE'}),
            {'r': ['L12345',], 'locale': 'de_DE', 'fmt': 'json'}),
        (  # Default provisional is filtered out
            (['L12345',], {'provisional': False}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Value for provisional is included
            (['L12345',], {'provisional': True}),
            {'r': ['L12345',], 'includeProvisional': 'true', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            (['L12345',], {'detail': 'simple'}),
            {'r': ['L12345',], 'fmt': 'json'}),
        (  # Value for hotspot is included
            (['L12345',], {'detail': 'full'}),
            {'r': ['L12345',], 'detail': 'full', 'fmt': 'json'}),
    ]

    validation = [
        (('L',), {}),  # location code is invalid
        (('',), {}),  # location code is blank
        (('L12345',), {'back': 31}),  # back is more than 30
        (('L12345',), {'back': 0}),  # back is less than 1
        (('L12345',), {'back': 'str'}),  # back cannot be converted to an integer
        (('L12345',), {'max_results': 10001}),  # max_results is more than 10000
        (('L12345',), {'max_results': 0}),  # max_results is less than 1
        (('L12345',), {'max_results': 'str'}),  # max_results is not an integer
        (('L12345',), {'locale': 'enUS'}),  # locale is not valid
        (('L12345',), {'locale': ''}),  # locale is blank
        # TODO Currently do not have validation tests for provisional
        (('L12345',), {'detail': 'complex'}),  # detail is not a recognised value
        (('L12345',), {'detail': ''}),  # detail is blank
    ]

    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        hotspot_observations('L12345')
        actual = mocked_function.call_args[0][0]
        self.assertEqual(HOTSPOT_OBSERVATIONS_URL, actual)

    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, ((args, kwargs), expected) in enumerate(self.parameters):
            hotspot_observations(*args, **kwargs)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.data.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, (args, kwargs) in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                hotspot_observations(*args, **kwargs)
