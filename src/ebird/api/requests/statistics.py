"""Functions for fetching basic statistics about observers and observations."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import (
    clean_area,
    clean_date,
    clean_max_observers,
    clean_rank,
    clean_region,
)

TOP_100_URL = "https://api.ebird.org/v2/product/top100/%s/%s"
TOTALS_URL = "https://api.ebird.org/v2/product/stats/%s/%s"


def get_top_100(token, region, date, rank="spp", max_results=100):
    """
    Get the observers who have seen the most species or submitted the
    greatest number of checklists on a given date.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#2d8d3f94-c4b0-42bd-9c8e-71edfa6347ba

    :param token: the token needed to access the API.

    :param region: the code for the region, eg. US-NV.

    :param date: the date, since Jan 1st 1800.

    :param rank: order results by species seen (spp) or checklists submitted (cl).

    :param max_results: the maximum number of entries to return from
    1 to 100. The default value is 100.

    :return: the list of observers.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TOP_100_URL % (clean_region(region), date.strftime("%Y/%m/%d"))

    params = {
        "maxObservers": clean_max_observers(max_results),
        "rankedBy": clean_rank(rank),
    }

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_totals(token, area, date):
    """
    Get the number of contributors, checklists submitted and species seen
    on a given date.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#4416a7cc-623b-4340-ab01-80c599ede73e

    :param token: the token needed to access the API.

    :param area: the code for a country subnational1 , subnational2 region
    or location

    :param date: the date, since Jan 1st 1800.

    :return: the totals for the given date

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TOTALS_URL % (clean_area(area), clean_date(date))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)
