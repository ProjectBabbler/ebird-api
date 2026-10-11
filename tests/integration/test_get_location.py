from ebird.api.requests import get_location


def test_get_hotspot(api_token):
    identifier = "L901738"
    details = get_location(api_token, identifier)
    assert details["locId"] == identifier


def test_get_private_location(api_token):
    identifier = "L8978128"
    details = get_location(api_token, identifier)
    assert details["locId"] == identifier
