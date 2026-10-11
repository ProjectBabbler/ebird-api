import datetime as dt

from ebird.api.requests import get_top_100


def test_api_call(api_token, subnational1_code):
    this_year = dt.date.today().replace(month=1, day=1)
    observers = get_top_100(api_token, subnational1_code, this_year)
    assert observers[0]["rowNum"] == 1
