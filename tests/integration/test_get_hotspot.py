from json import JSONDecodeError

import pytest

from ebird.api.requests import get_hotspot, get_hotspots


def test_api_call(api_token, subnational1_code):
    hotspots = get_hotspots(api_token, subnational1_code)
    location = get_hotspot(api_token, hotspots[0]["locId"])
    assert location["subnational1Code"] == subnational1_code


def test_get_hotspot_with_private_location_raises_error(api_token):
    identifier = "L8978128"
    with pytest.raises(JSONDecodeError):
        get_hotspot(api_token, identifier)
