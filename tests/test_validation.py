# -*- coding: utf-8 -*-

import unittest

from ebird.api import validation


class ValidationTests(unittest.TestCase):
    """Tests for the functions used to validate arguments."""

    def test_lat_string(self):
        """A value for lat return '[]'ed as a string in converted to a float."""
        self.assertEqual('45.34', validation.validate_lat('45.34'))

    def test_lat_max(self):
        """If the latitude is greater than 90 then an exception is raised."""
        self.assertRaises(ValueError, validation.validate_lat, 90.01)

    def test_lat_min(self):
        """If the latitude is less than -90 then an exception is raised."""
        self.assertRaises(ValueError, validation.validate_lat, -90.01)

    def test_lat_precision(self):
        """The latitude will be rounded 2 decimal places."""
        self.assertEqual('74.34', validation.validate_lat(74.336))

    def test_lng_string(self):
        """A value for lng return '[]'ed as a string in converted to a float."""
        self.assertEqual('45.34', validation.validate_lng('45.34'))

    def test_lng_max(self):
        """If the longitude is greater than 180 then an exception is raised."""
        self.assertRaises(ValueError, validation.validate_lng, 180.01)

    def test_lng_min(self):
        """If the longitude is less than -180 then an exception is raised."""
        self.assertRaises(ValueError, validation.validate_lng, -180.01)

    def test_lng_precision(self):
        """The longitude will be rounded 2 decimal places."""
        self.assertEqual('74.34', validation.validate_lng(74.344))

    def test_dist_string(self):
        """A value for dist return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, validation.validate_dist('10'))

    def test_dist_min(self):
        """If the dist is less than zero an exception is raised."""
        self.assertRaises(ValueError, validation.validate_dist, -1)

    def test_dist_max(self):
        """If the dist is more than 50 an exception is raised."""
        self.assertRaises(ValueError, validation.validate_dist, 51)

    def test_back_string(self):
        """A value for back return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, validation.validate_back('10'))

    def test_back_min(self):
        """If back is less than one an exception is raised."""
        self.assertRaises(ValueError, validation.validate_back, 0)

    def test_back_max(self):
        """If back is more than 30 an exception is raised."""
        self.assertRaises(ValueError, validation.validate_back, 31)

    def test_max_results_none(self):
        """A value of None for max_results is valid"""
        self.assertEqual(None, validation.validate_max_results(None, 10000))

    def test_max_results_string(self):
        """A value for max_results return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, validation.validate_max_results('10', 10000))

    def test_max_results_min(self):
        """If max_results is less than one an exception is raised."""
        self.assertRaises(ValueError, validation.validate_max_results, 0, 10000)

    def test_max_results_max(self):
        """If max_results is more than the limit an exception is raised."""
        self.assertRaises(ValueError, validation.validate_max_results, 10001, 10000)

    def test_locale_invalid(self):
        """If the locale is not in the form xx_YY and exception is raised."""
        self.assertRaises(ValueError, validation.validate_locale, 'enUS')

    def test_locale_case(self):
        """The case of the locale is changed is necessary."""
        self.assertEqual('en_US', validation.validate_locale('EN_us'))
