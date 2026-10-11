from ebird.api.requests import get_nearby_notable


def test_api_call(api_token, coordinates):
    observations = get_nearby_notable(api_token, coordinates[0], coordinates[1])
    assert "speciesCode" in observations[0]
    assert "locId" in observations[0]
    assert "subId" in observations[0]
