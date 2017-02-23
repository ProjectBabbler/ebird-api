# -*- coding: utf-8 -*-

"""Wrappers for the end-points returning aggregated data from the eBird API.

    hotspot_summary() - get a summary of the species seen recently at a list of hotspots.

"""

from ebird.api.base import get_json, get_content, filter_parameters

from ebird.api.validation import  validate_locations, validate_back, \
    validate_max_results, validate_locale, validate_provisional, validate_detail


HOTSPOT_SUMMARY_URL = 'http://ebird.org/ws1.1/product/obs/hotspot/recent'


def hotspot_summary(codes, back=14, max_results=None, locale='en_US',
                    provisional=False, detail='simple'):
    """Get a summary of the species seen recently at a list of hotspots.

    Get a summary of the recent observations (up to 30 days ago) from up
    to 10 hotspots.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotspotSightingsSummary

    NOTE: This function is identical to hotspot_observations() except that
    the records return contain an additional field that contains the number
    of checklists that recorded a given species.

    :param codes: the unique identifiers, eg. L3733278 of up to 10 hotspots.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param provisional: include records which have not yet been reviewed.
    Either True or False, the default is False.

    :param detail: return records in 'simple' or 'full' format. See the eBird API
    documentation for a description of the fields.

    :return: the list of observations.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        'r': validate_locations(codes),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_json(get_content(
        HOTSPOT_SUMMARY_URL, filter_parameters(params)))
