import datetime as dt

from ebird.api.requests import get_totals


def test_api_call(api_token, subnational1_code):
    totals = get_totals(api_token, subnational1_code, dt.date.today())
    assert "numChecklists" in totals
    assert "numContributors" in totals
    assert "numSpecies" in totals
