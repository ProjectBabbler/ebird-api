# -*- coding: utf-8 -*-

"""Various utility functions used in the API.

These are also pretty useful if you want to write your own
high-level functions.

"""

import re

from ebird.core import region_observations, geo_observations


def find_locations(observations):
    """Get the list of location codes from a list of observations.

    :param observations: the list of observations.

    :return: a list of location codes found in the observations. Each
    location only appears once in the list.

    """
    locations = set()
    for observation in observations:
        code = observation.get('locID', None)
        if code:
            locations.add(code)
    return list(locations)


def find_locations_in_area(point, back=14):
    """Get the list of locations in an area.

    :param point: the coordinates and optional radius.
    :type point: dict

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :return: the list of unique identifiers for locations.
    :rtype: list

    """
    params = {'back': back, 'provisional': True}
    params.update(point)
    return find_locations(geo_observations(**params))


def find_locations_in_region(code, back=14):
    """Get the list of locations in a region.

    :param code: the code for the county or region/state.
    :type code: str

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :return: the list of unique identifiers for locations.
    :rtype: list

    """
    return find_locations(
        region_observations(code, back=back, provisional=True))


def is_point(value):
    """Does the value represent a set of coordinates?

    :param value: the value to check

    :return: True if the value is a set of coordinates, False otherwise.

    """
    return type(value) == dict and 'lat' in value and 'lng' in value


def is_region(value):
    """Does the value represent a region or county?

    :param value: the value to check

    :return: True if the value is the code for a region or county,
    False otherwise.

    """
    return type(value) == str and re.match(r'^\w{2}-\w{2}(-\w{2,})?$', value)


def is_location(value):
    """Does the value represent a specific location?

    :param value: the value to check

    :return: True if the value is the code for a location, False otherwise.

    """
    return type(value) == str and re.match(r'^L\w{5,}$', value)


def filter_points(sites):
    """Get all the sets of coordinates from the list of sites.

    :param sites: the list of sites to check.

    :return: the list of coordinates found.
    :rtype: list

    """
    return [site for site in sites if is_point(site)]


def filter_regions(sites):
    """Get all the codes for regions from the list of sites.

    :param sites: the list of sites to check.

    :return: the list of region codes found.
    :rtype: list

    """
    return [site for site in sites if is_region(site)]


def filter_locations(sites):
    """Get all the codes for locations from the list of sites.

    :param sites: the list of sites to check.

    :return: the list of location codes found.
    :rtype: list

    """
    return [site for site in sites if is_location(site)]


def split_list(values, size):
    """Yield successive groups of items from a list.

    The API for fetching records from hotspots or locations can only
    deal with up 10 locations at a time. This function breaks a list
    into block of 10 items so with a loop you can get observations for
    any number of locations.

    :param values: a list of codes for locations or hotspots.
    :param values: list

    :param size: the number of items to include in each sublist.
    :type size: int

    :returns: the original list of values split into lists of size items.
    :rtype: list

    """
    for i in range(0, len(values), size):
        yield values[i:i + size]


def nest(records):
    """Created a nested version from the flat record structure from eBird.

    The records returned from eBird (both 'simple' and 'full' formats) are
    flat lists of key-value pairs. nest() creates a nested dict with
    groups of related parameters, specifically with the fields for species
    and location. That makes it easy to load the records into a database.

    :param records: the records returned from eBird.
    :type records: list

    :returns: a list with the fields for species and location grouped into
    nested dicts.
    :rtype: list

    """
    results = []
    for record in records:
        results.append({
            'identifier': record['obsID'],
            'date': record['obsDt'],
            'species': {
                'common': record['comName'],
                'scientific': record['sciName'],
            },
            'count': record['howMany'] if 'howMany' in record else 0,
            'present': record['presenceNoted'],
            'location': {
                'identifier': record['locID'],
                'private': record['locationPrivate'],
                'name': record['locName'],
                'lat': record['lat'],
                'lng': record['lng'],
                'county': record['subnational2Name'],
                'county_code': record['subnational2Code'],
                'state': record['subnational1Name'],
                'state_code': record['subnational1Code'],
                'country': record['countryName'],
                'country_code': record['countryCode'],
            },
            'observer': record['userDisplayName'],
            'reviewed': record['obsReviewed'],
            'valid': record['obsValid'],
            'submission': record['subID'],
            'checklist': record['checklistID'],
        })
    return results