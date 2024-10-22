from ebird.api import get_hotspot, get_hotspots


def test_api_call(api_token, subnational1_code):
    hotspots = get_hotspots(api_token, subnational1_code)
    location = get_hotspot(api_token, hotspots[0]["locId"])
    assert location["subnational1Code"] == subnational1_code
