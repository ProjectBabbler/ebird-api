from ebird.api.requests import get_hotspots


def test_api_call(api_token, subnational1_code):
    hotspots = get_hotspots(api_token, subnational1_code)
    expected = [subnational1_code] * len(hotspots)
    actual = [hotspot["subnational1Code"] for hotspot in hotspots]
    assert actual == expected
