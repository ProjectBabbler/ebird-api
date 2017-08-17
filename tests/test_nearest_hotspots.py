# -*- coding: utf-8 -*-

from unittest import TestCase, mock

from ebird.api.reference import NEAREST_HOTSPOTS_URL, nearest_hotspots


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class NearestHotspotsTests(TestCase):
    """Tests for the nearest_hotspots() API call.

    We are using positional arguments to make the test patterns easier
    to read.

    """
    parameters = [
        ((0.0, 1.0, 10, None), {'lat': '0.00', 'lng': '1.00', 'dist': 10}),
        ((0.0, 1.0, 25, None), {'lat': '0.00', 'lng': '1.00'}),
        ((0.0, 1.0, 25, 10), {'lat': '0.00', 'lng': '1.00', 'back': 10}),
    ]

    validation = [
        # Latitude is less than -90
        (-90.01, 0.0),
        # Latitude is greater than 90
        (90.01, 0.0),
        # Longitude is less than -180
        (0.0, -180.01),
        # Longitude is greater than 180
        (0.0, 180.01),
        # Dist is less than 0.
        (0.0, 0.0, -1),
        # Dist is greater than 50.
        (0.0, 0.0, 51),
        # Back is less than 1.
        (0.0, 0.0, 25, 0),
        # Back is greater than 30.
        (0.0, 0.0, 25, 31)
    ]

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        nearest_hotspots(0.0, 0.0)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(NEAREST_HOTSPOTS_URL, actual)

    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (args, expected) in enumerate(self.parameters):
            nearest_hotspots(*args)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.api.reference.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, args in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                nearest_hotspots(*args)
