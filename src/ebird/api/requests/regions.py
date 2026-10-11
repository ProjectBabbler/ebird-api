"""Functions for fetching information about regions."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import clean_region, clean_region_type

REGION_LIST_URL = "https://api.ebird.org/v2/ref/region/list/%s/%s"
ADJACENT_REGIONS_URL = "https://api.ebird.org/v2/ref/adjacent/%s"
REGION_INFO_URL = "https://api.ebird.org/v2/ref/region/info/%s"


def get_regions(token, rtype, region):
    """Get the list of sub-regions or a given region.

    This maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#e25218db-566b-4d8b-81ca-e79a8f68c599

    Not all combinations of region type and region code are supported.
    You can get all the subnational2 regions of a country but you cannot
    get the subnational2 regions for the world.

    :param token: the token needed to access the API.

    :param rtype: the region type, either 'country', 'subnational1'
    or 'subnational2'.

    :param region: the name of the region, either 'world', a country or
    a subnational1 code.

    :return: the list of sub-regions within the given region.

    :raises ValueError: if an invalid region type is given.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = REGION_LIST_URL % (clean_region_type(rtype), clean_region(region))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)


def get_adjacent_regions(token, region):
    """Get the regions adjacent to a given region.

    This maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#3aca0519-3105-47fc-8611-a4dfd500a32f

    :param token: the token needed to access the API.

    :param region: the name of the region, either a country, a subnational1
    or a subnational2 code.

    :return: the list of regions bordering the specified region.

    :raises ValueError: if an invalid region code.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = ADJACENT_REGIONS_URL % clean_region(region)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)


def get_region(token, region):
    """Get the geographical details of a country, region or sub-region.

    This maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#e25218db-566b-4d8b-81ca-e79a8f68c599

    There are two query parameters supported by the API, regionNameFormat
    and delim. These are used to control how the name of the region that the
    region code corresponds to is presented, e.g. US-NY returns "New York,
    United States". The utility of these is rather limited so they are
    currently not supported.

    :param token: the token needed to access the API.

    :param region: the code for the region, eg. US-NV.

    :return: the latitude, longitude, name, region, etc. for the area.

    :raises ValueError: if an invalid region code is given.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = REGION_INFO_URL % clean_region(region)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)
