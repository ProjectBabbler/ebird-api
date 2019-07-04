"""Functions for fetching information about hotspots."""

from ebird.api.utils import call

from ebird.api.validation import clean_lat, clean_lng, clean_dist, \
    clean_back, clean_region, clean_location

REGION_HOTSPOTS_URL = 'https://ebird.org/ws2.0/ref/hotspot/%s'
NEARBY_HOTSPOTS_URL = 'https://ebird.org/ws2.0/ref/hotspot/geo'
HOTSPOT_INFO_URL = 'https://ebird.org/ws2.0/ref/hotspot/info/%s'


def get_hotspots(token, region, back=None):
    """List all hotspots within a region.

    If back is specified then only the hotspots visited in the given number
    of days are returned.

    Fetch all the hotspots visited in  country, subnational1 or subnational2
    area recently (up to 30 days ago).

    This maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#f4f59f90-854e-4ba6-8207-323a8cf0bfe0

    The API supports the option of returning records either in JSON or
    CSV format. Currently results are always returned in JSON format
    since that is consistent with the other functions.

    :param token: the token needed to access the API.

    :param region: the code for a country, subnational1 or subnational2 region.

    :param back: the past number of days to check, default is 14.

    :return: the list of hotspots.

    :raises ValueError: if an invalid region code is given or if the value for
    'back', if given, is not in the range 1..30.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = REGION_HOTSPOTS_URL % clean_region(region)

    params = {
        'fmt': 'json'
    }

    if back is not None:
        params['back'] = clean_back(back)

    headers = {
        'X-eBirdApiToken': token,
    }

    return call(url, params, headers)


def get_nearby_hotspots(token, lat, lng, dist=25, back=None):
    """Get the list of nearby hotspots.

    Get the list of hotspots closest to a set of coordinates (latitude,
    longitude) up to a distance of 50km. If back is specified then only
    the hotspots visited in the given number of days are returned.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#674e81c1-6a0c-4836-8a7e-6ea1fe8e6677

    The API supports the option of returning records either in JSON or
    CSV format. Currently results are always returned in JSON format
    since that is consistent with the other functions.

    :param token: the token needed to access the API.

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

    :param back: include only visits to the hotspots from 1 to 30 days.
    The default value of None will include all hotspots.

    :return: the list of hotspots nearest to the given set of coordinates.

    :raises ValueError: if the coordinates are out of range, if the value
    for 'dist' is not in the range 1..50 or if the value for 'back', if
    specified, is not in the range 1..30.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        'lat': clean_lat(lat),
        'lng': clean_lng(lng),
        'dist': clean_dist(dist),
        'fmt': 'json'
    }

    if back is not None:
        params['back'] = clean_back(back)

    headers = {
        'X-eBirdApiToken': token,
    }

    return call(NEARBY_HOTSPOTS_URL, params, headers)


def get_hotspot(token, loc_id):
    """Get the geographical details of a hotspot.

    This maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#e25218db-566b-4d8b-81ca-e79a8f68c599

    :param token: the token needed to access the API.

    :param loc_id: the location code for a hotspot, eg. L374326.

    :return: the latitude, longitude, name, region, etc. for the hotspot.

    :raises ValueError: if an invalid location code is given.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = HOTSPOT_INFO_URL % clean_location(loc_id)

    headers = {
        'X-eBirdApiToken': token,
    }

    return call(url, {}, headers)
