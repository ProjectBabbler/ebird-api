import geopy.distance

from ebird.api.requests import get_nearby_hotspots


def test_api_call(api_token, coordinates):
    hotspots = get_nearby_hotspots(api_token, coordinates[0], coordinates[1])
    for hotspot in hotspots:
        hotspot_coordinates = (hotspot["lat"], hotspot["lng"])
        assert geopy.distance.geodesic(coordinates, hotspot_coordinates).km <= 50
