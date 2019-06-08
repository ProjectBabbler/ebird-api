# -*- coding: utf-8 -*-

"""Various functions used in the API."""

import csv
import json
import re

from urllib.request import Request, urlopen
from urllib.parse import urlencode


# default values for the query parameters sent to the eBird API.
# There is no value for maxResults as this varies according to
# the type of API call being made. The individual functions will
# add a default value to filter.

PARAMETER_DEFAULTS = {
    'back': 14,
    'cat': None,
    'detail': 'simple',
    'dist': 25,
    'groupNameLocale': 'en',
    'hotspot': 'false',
    'includeProvisional': 'false',
    'locale': 'en',
    'sort': 'date',
    'sppLocale': 'en',
}


def filter_parameters(params, **kwargs):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :param kwargs: additional values to use to filter out default values.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    result = {}

    defaults = PARAMETER_DEFAULTS.copy()
    defaults.update(**kwargs)

    for key, value in params.items():
        if key in defaults:
            if value != defaults[key]:
                result[key] = value
        else:
            result[key] = value

    return result


def get_content(url, params, headers):
    """Get the content from the eBird API.

    :param url: the URL for the API call.
    :type url: str

    :param params: the query parameters for the API call.
    :type params: dict

    :param headers: the headers to add to the request.
    :type params: dict

    :return: the content returned by the API
    :rtype: str

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    request = Request(url + '?' + urlencode(params, doseq=True))
    for name, value in headers.items():
        request.add_header(name, value)
    return urlopen(request).read().decode('utf-8')


def get_json(content):
    """Decode the JSON records from the response.

    :param content: the content returned by the eBird API.
    :type response:

    :return: the records decoded from the JSON payload.
    :rtype: list

    """
    return json.loads(content)


def get_csv(content):
    """Decode the CSV records from the response.

    :param content: the content returned by the eBird API.
    :type response:

    :return: the records decoded from the CSV payload.
    :rtype: list

    """
    return list(csv.DictReader(content.splitlines(), delimiter=','))


def region_type_for_code(value):
    """Get the region type for the code.

    :param value: the code for a country, subnational1 or subnational2
    region, e.g 'US', 'US-NV' or 'US-NV-001'
    :type value: str

    :returns: a string describing the type of the code, either 'country',
    'subnational1' or 'subnational2'

    """
    cleaned = value.upper()
    if re.match(r'^[A-Z]{2}$', cleaned):
        rtype = 'country'
    elif re.match(r'^[A-Z]{2}-\w{2,}$', cleaned):
        rtype = 'subnational1'
    elif re.match(r'^[A-Z]{2}-\w{2,}-\w{2,}$', cleaned):
        rtype = 'subnational2'
    else:
        raise ValueError("Value must be a country, e.g. 'US', subnational1 code, "
                         "e.g. 'US-NV' or subnational2 code, e.g. 'US-NV-211'")

    return rtype
