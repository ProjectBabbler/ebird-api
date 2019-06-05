# -*- coding: utf-8 -*-

from ebird.api.base import get_json, get_content, filter_parameters

from ebird.api.utils import clean_area, clean_date, clean_max_results, clean_region


TOP_100_URL = 'https://ebird.org/ws2.0/product/top100/%s/%s'
TOTALS_URL = 'https://ebird.org/ws2.0/product/stats/%s/%s'


def get_top_100(token, region, date, max_results=100):
    """
    ???

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#2d8d3f94-c4b0-42bd-9c8e-71edfa6347ba

    :param token: the token needed to access the API.

    :param region: the code for the region, eg. US-NV.

    :param date: the date, since Jan 1st 1800.

    :param max_results: the maximum number of entries to return from
    1 to 100. The default value is 100.

    :return:

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TOP_100_URL % (
        clean_region(region), date.strftime('%Y/%m/%d'))

    params = {
        'maxResults': clean_max_results(max_results, 100),
        'checklistSort': False,
    }

    defaults = {
        'maxResults': 100
    }

    headers = {
        'X-eBirdApiToken': token,
    }

    return get_json(get_content(url, filter_parameters(params, **defaults), headers))


def get_totals(token, area, date):
    """
    Get the number of contributors, checklists submitted and species seen on a given date.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#4416a7cc-623b-4340-ab01-80c599ede73e

    :param token: the token needed to access the API.

    :param area: the code for a country subnational1 , subnational2 region or location

    :param date: the date, since Jan 1st 1800.

    :return: the totals for the given date

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TOTALS_URL % (
        clean_area(area), clean_date(date))

    headers = {
        'X-eBirdApiToken': token,
    }

    return get_json(get_content(url, {}, headers))
