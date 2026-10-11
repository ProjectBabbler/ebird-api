"""Functions for fetching checklists and information about visits."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import (
    clean_area,
    clean_code,
    clean_date,
    clean_max_checklists,
)

CHECKLISTS_DATE_URL = "https://api.ebird.org/v2/product/lists/%s/%s"
CHECKLISTS_RECENT_URL = "https://api.ebird.org/v2/product/lists/%s"
CHECKLIST_URL = "https://api.ebird.org/v2/product/checklist/view/%s"


def get_visits(token, area, date=None, max_results=10):
    """
    Get the list of checklists for an area. The most recent checklists are
    returned if a specific date is not given.

    The maps to the two end points in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#4416a7cc-623b-4340-ab01-80c599ede73e
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#95a206d1-a20d-44e0-8c27-acb09ccbea1a
    which return results in the same format.

    The eBird API call also has a sortKey parameter which returns records
    ordered by observation date or by creation date. Since checklists are
    often submitted a few days after the actual visit this parameter is
    not currently supported. The results are returned ordered by observation
    date.

    :param token: the token needed to access the API.

    :param area: the code for a country, subnational1 region, subnational2
    region or location.

    :param date: the date, since Jan 1st 1800.

    :param max_results: the maximum number of checklists to return from
    1 to 200. The default value is 10.

    :return: the info for all the checklists submitted.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    if date is not None:
        url = CHECKLISTS_DATE_URL % (clean_area(area), clean_date(date))
    else:
        url = CHECKLISTS_RECENT_URL % clean_area(area)

    params = {
        "maxVisits": clean_max_checklists(max_results),
        "sortKey": "obs_dt",
    }

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_checklist(token, sub_id):
    """
    Get the contents of a checklist.

    The information returned include the checklist attributes, date, etc. and the
    list of observations. Only the code for the location and subnational1 are
    included you will need to call get_hotspot_info() to get the full details
    of the location.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#4416a7cc-623b-4340-ab01-80c599ede73e

    :param token: the token needed to access the API.

    :param sub_id: the unique identifier for the checklist, e.g. S22893621.

    :return: the details of the checklist, including the list of observations

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = CHECKLIST_URL % clean_code(sub_id)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)
