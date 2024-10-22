from ebird.api import get_adjacent_regions


def test_api_call(api_token, subnational1_code):
    regions = get_adjacent_regions(api_token, subnational1_code)
    expected = ["US-CT", "US-NH", "US-NY", "US-RI", "US-VT"]
    actual = [region["code"] for region in regions]
    assert sorted(expected) == sorted(actual)
