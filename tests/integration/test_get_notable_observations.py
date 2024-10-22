from ebird.api import get_notable_observations


def test_api_call(api_token, subnational1_code):
    observations = get_notable_observations(api_token, subnational1_code)
    assert "speciesCode" in observations[0]
    assert "locId" in observations[0]
    assert "subId" in observations[0]
