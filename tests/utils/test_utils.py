# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

import unittest

from ebird.api import utils


class ValidationTests(unittest.TestCase):
    """Tests for the functions used to validate arguments."""

    def test_is_country(self):
        self.assertTrue(utils.is_country('US'))

    def test_incomplete_country(self):
        self.assertFalse(utils.is_country('U'))

    def test_is_subnational1(self):
        self.assertTrue(utils.is_subnational1('US-NV'))

    def test_incomplete_subnational1(self):
        self.assertFalse(utils.is_subnational1('US-'))

    def test_is_subnational2(self):
        self.assertTrue(utils.is_subnational2('US-NV-VMT'))

    def test_incomplete_subnational2(self):
        self.assertFalse(utils.is_subnational2('US-NV-'))

    def test_lat_string(self):
        """A value for lat return '[]'ed as a string in converted to a float."""
        self.assertEqual('45.34', utils.clean_lat('45.34'))

    def test_lat_max(self):
        """If the latitude is greater than 90 then an exception is raised."""
        self.assertRaises(ValueError, utils.clean_lat, 90.01)

    def test_lat_min(self):
        """If the latitude is less than -90 then an exception is raised."""
        self.assertRaises(ValueError, utils.clean_lat, -90.01)

    def test_lat_precision(self):
        """The latitude will be rounded 2 decimal places."""
        self.assertEqual('74.34', utils.clean_lat(74.336))

    def test_lng_string(self):
        """A value for lng return '[]'ed as a string in converted to a float."""
        self.assertEqual('45.34', utils.clean_lng('45.34'))

    def test_lng_max(self):
        """If the longitude is greater than 180 then an exception is raised."""
        self.assertRaises(ValueError, utils.clean_lng, 180.01)

    def test_lng_min(self):
        """If the longitude is less than -180 then an exception is raised."""
        self.assertRaises(ValueError, utils.clean_lng, -180.01)

    def test_lng_precision(self):
        """The longitude will be rounded 2 decimal places."""
        self.assertEqual('74.34', utils.clean_lng(74.344))

    def test_dist_string(self):
        """A value for dist return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, utils.clean_dist('10'))

    def test_dist_min(self):
        """If the dist is less than zero an exception is raised."""
        self.assertRaises(ValueError, utils.clean_dist, -1)

    def test_dist_max(self):
        """If the dist is more than 50 an exception is raised."""
        self.assertRaises(ValueError, utils.clean_dist, 51)

    def test_back_string(self):
        """A value for back return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, utils.clean_back('10'))

    def test_back_min(self):
        """If back is less than one an exception is raised."""
        self.assertRaises(ValueError, utils.clean_back, 0)

    def test_back_max(self):
        """If back is more than 30 an exception is raised."""
        self.assertRaises(ValueError, utils.clean_back, 31)

    def test_max_results_none(self):
        """A value of None for max_results is valid"""
        self.assertEqual(None, utils.clean_max_results(None, 10000))

    def test_max_results_string(self):
        """A value for max_results return '[]'ed as a string in converted to an integer."""
        self.assertEqual(10, utils.clean_max_results('10', 10000))

    def test_max_results_min(self):
        """If max_results is less than one an exception is raised."""
        self.assertRaises(ValueError, utils.clean_max_results, 0, 10000)

    def test_max_results_max(self):
        """If max_results is more than the limit an exception is raised."""
        self.assertRaises(ValueError, utils.clean_max_results, 10001, 10000)

    def test_locale_invalid(self):
        """If the locale is not in the form xx_YY and exception is raised."""
        self.assertRaises(ValueError, utils.clean_locale, 'enUS')

    def test_locale_case(self):
        """The case of the locale is changed is necessary."""
        self.assertEqual('en_US', utils.clean_locale('EN_us'))

    def test_clean_date_string(self):
        self.assertEqual('2019/05/31', utils.clean_date('2019-05-31'))

    def test_clean_invalid_date_string(self):
        self.assertRaises(ValueError, utils.clean_date, '31/05/2019')

    def test_clean_date(self):
        self.assertEqual('2019/05/31', utils.clean_date(date(2019, 5, 31)))

    def test_clean_datetime(self):
        self.assertEqual('2019/05/31', utils.clean_date(datetime(2019, 5, 31)))

    def test_clean_date_before_1800(self):
        self.assertRaises(ValueError, utils.clean_date, date(1799, 12, 31))

    def test_clean_future_date(self):
        self.assertRaises(ValueError, utils.clean_date, datetime.today() + timedelta(days=1))
