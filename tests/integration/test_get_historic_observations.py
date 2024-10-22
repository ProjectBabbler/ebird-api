import datetime as dt

from ebird.api import get_historic_observations


def test_api_call(api_token, subnational1_code):
    observations = get_historic_observations(
        api_token, subnational1_code, dt.date.today()
    )
    assert "speciesCode" in observations[0]
    assert "locId" in observations[0]
    assert "subId" in observations[0]
