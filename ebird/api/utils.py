"""Various functions used in the API."""

import json

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
    'sort': constants.DEFAULT_OBSERVATION_ORDER,
    'sppLocale': constants.DEFAULT_LOCALE,
    'maxObservations': constants.DEFAULT_MAX_OBSERVATIONS,
    'maxObservers': constants.DEFAULT_MAX_OBSERVERS,
    'maxVisits': constants.DEFAULT_MAX_CHECKLISTS,
    'rankedBy': constants.DEFAULT_TOP_100_RANK
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

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    mapped = {}

    for key, value in params.items():
        key = _parameter_map.get(key, key)
        mapped[key] = value

    return mapped


def filter_parameters(params):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    filtered = {}

    defaults = _parameter_defaults.copy()

    for key, value in params.items():
        if key in defaults:
            if value != defaults[key]:
                filtered[key] = value
        else:
            filtered[key] = value

    return filtered


def get_response(url, params=None, headers=None):
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
    if params:
        url += '?' + urlencode(params, doseq=True)

    request = Request(url)

    if headers:
        for name, value in headers.items():
            request.add_header(name, value)

    return urlopen(request).read()


def get_json(content):
    """Decode the JSON records from the response.

    :param content: the content returned by the eBird API.
    :type content: http.client.HTTPResponse:

    :return: the records decoded from the JSON payload.
    :rtype: list

    """
    return json.loads(content.decode('utf-8'))


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


def call(url, params, headers):
    """Call the eBird API.

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
    filtered = filter_parameters(params)
    mapped = map_parameters(filtered)
    return get_json(get_response(url, mapped, headers))
