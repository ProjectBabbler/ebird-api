from ebird.api.requests import get_observations


def test_api_call(api_token, subnational1_code):
    observations = get_observations(api_token, subnational1_code)
    assert "speciesCode" in observations[0]
    assert "locId" in observations[0]
    assert "subId" in observations[0]
