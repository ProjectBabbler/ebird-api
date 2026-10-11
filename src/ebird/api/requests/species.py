"""Functions for fetching information about species."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import clean_area

SPECIES_LIST_URL = "https://api.ebird.org/v2/product/spplist/%s"


def get_species_list(token, area):
    """
    Get the list of species for an area.

    The maps to the two end points in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#55bd1b26-6951-4a88-943a-d3a8aa1157dd

    :param token: the token needed to access the API.

    :param area: the code for a country, subnational1 region, subnational2
    region or location.

    :return: codes, e.g. horlar1, for the list of species observed in the area.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = SPECIES_LIST_URL % clean_area(area)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)
