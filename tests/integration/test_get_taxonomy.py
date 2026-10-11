from ebird.api.requests import get_taxonomy


def test_api_call(api_token):
    result = get_taxonomy(api_token, locale="de")
    assert result[0]["comName"] == "Strauß"  # ostrich
