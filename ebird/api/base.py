# -*- coding: utf-8 -*-

"""Various functions used in the API."""

import csv
import json
import re

from urllib import request
from urllib.parse import urlencode


# default values for the query parameters sent to the eBird API.

PARAMETER_DEFAULTS = {
    'back': 14,
    'dist': 25,
    'maxResults': None,
    'hotspot': 'false',
    'includeProvisional': 'false',
    'locale': 'en_US',
    'fmt': 'xml',
    'detail': 'simple',
    'cat': 'species',
}


def filter_parameters(params):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    result = {}
    for key, value in params.items():
        if key in PARAMETER_DEFAULTS:
            if value != PARAMETER_DEFAULTS[key]:
                result[key] = value
        else:
            result[key] = value

    return result


def get_content(url, params):
    """Get the content from the eBird API.

    :param url: the URL for the API call.
    :type url: str

    :param params: the query parameters for the API call.
    :type params: dict

    :return: the content returned by the API
    :rtype: str

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    response = request.urlopen(url + '?' + urlencode(params, doseq=True))
    return response.read().decode('utf-8')


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
        return 'country'
    elif re.match(r'[A-Z]{2}-\w{2,}$', cleaned):
        return 'subnational1'
    elif re.match(r'^\w{2}-\w{2,}-\w{2,}$', cleaned):
        return 'subnational2'
    else:
        raise ValueError(
            "Value must be a country, e.g. 'US', subnational1 code, "
            "e.g. 'US-NV' or subnational2 code, e.g. 'US-NV-211'")
