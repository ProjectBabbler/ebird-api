import unittest
from datetime import date, datetime, timedelta

from ebird.api.requests.validation import clean_date


class CleanDateTests(unittest.TestCase):
    """Tests for the clean_date validation function."""

    def test_date_string(self):
        self.assertEqual("2019/05/31", clean_date("2019-05-31"))

    def test_invalid_date_string(self):
        self.assertRaises(ValueError, clean_date, "31/05/2019")

    def test_date(self):
        self.assertEqual("2019/05/31", clean_date(date(2019, 5, 31)))

    def test_datetime(self):
        self.assertEqual("2019/05/31", clean_date(datetime(2019, 5, 31)))

    def test_date_before_1800(self):
        self.assertRaises(ValueError, clean_date, date(1799, 12, 31))

    def test_future_date(self):
        self.assertRaises(ValueError, clean_date, datetime.today() + timedelta(days=1))
