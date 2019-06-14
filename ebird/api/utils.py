# -*- coding: utf-8 -*-

"""Various functions used in the API."""

import csv
import json
import re

from urllib.request import Request, urlopen
from urllib.parse import urlencode

from ebird.api import constants


_parameter_defaults = {
    'back': constants.DEFAULT_BACK,
    'cat': constants.DEFAULT_SPECIES_CATEGORY,
    'detail': constants.DEFAULT_DETAIL,
    'dist': constants.DEFAULT_DISTANCE,
    'groupNameLocale': constants.DEFAULT_LOCALE,
    'hotspot': constants.DEFAULT_HOTSPOTS_ONLY,
    'includeProvisional': constants.DEFAULT_PROVISIONAL,
    'locale': constants.DEFAULT_LOCALE,
    'sort': constants.DEFAULT_OBSERVATION_ORDER,
    'sppLocale': constants.DEFAULT_LOCALE,
    'maxObservations': constants.DEFAULT_MAX_OBSERVATIONS,
    'maxObservers': constants.DEFAULT_MAX_OBSERVERS,
    'maxVisits': constants.DEFAULT_MAX_CHECKLISTS,
}

_parameter_map = {
    'maxObservations': 'maxResults',
    'maxObservers': 'maxResults',
    'maxVisits': 'maxResults',
}


def map_parameters(params):
    """Translate the names of the query parameters to match those used
    in the API.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :param kwargs: additional values to use to filter out default values.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    mapped = {}

    for key, value in params.items():
        key = _parameter_map.get(key, key)
        mapped[key] = value

    return mapped


def filter_parameters(params, **kwargs):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :param kwargs: additional values to use to filter out default values.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    filtered = {}

    defaults = _parameter_defaults.copy()
    defaults.update(**kwargs)

    for key, value in params.items():
        if key in defaults:
            if value != defaults[key]:
                filtered[key] = value
        else:
            filtered[key] = value

    return filtered


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
    :type content: http.client.HTTPResponse:

    :return: the records decoded from the JSON payload.
    :rtype: list

    """
    return json.loads(content)


def save_json(filename, data, indent=None):
    """Save results to a file.

    :param filename: the name of the file to save. The .json
    extension will be added if not present.

    :param data: the list of records to save.

    :param indent: whether to pretty-print results by adding indentation
    for each level. The default is no formatting.

    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=indent)


def get_csv(content):
    """Decode the CSV records from the response.

    :param content: the content returned by the eBird API.
    :type content: http.client.HTTPResponse:

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
