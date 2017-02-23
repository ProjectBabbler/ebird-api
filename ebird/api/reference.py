# -*- coding: utf-8 -*-

"""Wrappers for the end-points returning reference data from the eBird API.

    list_locations() - get the codes for countries, subnational1 or subnational2 areas.
    find_locations() - find countries, subnational1 or subnational2 areas that match a name.

    list_hotspots() - get the hotspots for a country, subnational1 or subnational2 area.
    nearest_hotspots() - get the list of nearby hotspots.

    list_species() - get the list of species in the eBird taxonomy.

"""

from ebird.api.base import region_type_for_code, get_csv, get_content, filter_parameters

from ebird.api.validation import validate_category, validate_locale, validate_lat, \
    validate_lng, validate_dist, validate_back, validate_region, validate_region_type


LIST_REGIONS_URL = 'http://ebird.org/ws1.1/ref/location/list'
FIND_REGIONS_URL = 'http://ebird.org/ws1.1/ref/location/find'
LIST_HOTSPOTS_URL = 'http://ebird.org/ws1.1/ref/hotspot/region'
NEAREST_HOTSPOTS_URL = 'http://ebird.org/ws1.1/ref/hotspot/geo'
LIST_SPECIES_URL = 'http://ebird.org/ws1.1/ref/taxa/ebird'


def list_hotspots(code, back=None):
    """List all hotspots visited recently within a region.

    Fetch all the hotspots visited in  country, subnational1 or subnational2
    area recently (up to 30 days ago). All hotspots are returned if the
    default value for the keyword arg, back, of None is used.

    This maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotspotReference

    :param code: the code for the region, eg. US-NV.

    :param back: include all hotspots of those visited up to 30 days ago.

    :return: the list of hotspots.

    :raises ValueError: if an invalid region code is given or if the value for
    'back' is not None or in the range 1..30.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        'r': validate_region(code),
    }

    if back is not None:
        params['back'] = validate_back(back)

    return get_csv(get_content(LIST_HOTSPOTS_URL, params))


def nearest_hotspots(lat, lng, dist=25, back=None):
    """Get the list of nearby hotspots.

    Get the list of hotspots closest to a set of coordinates (latitude,
    longitude) up to a distance of 50km.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotspotGeoReference

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

    :param back: include only visits to the hotspots from 1 to 30 days. The
    default value of None will include all hotspots.

    :return: the list of hotspots nearest to the given set of coordinates.

    :raises ValueError: if the coordinates are out of range, if the value
    for 'dist' is not in the range 1..50 or if the value for 'back' is not
    None or in the range 1..30.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        'lat': validate_lat(lat),
        'lng': validate_lng(lng),
    }

    if dist != 25:
        params['dist'] = validate_dist(dist)

    if back is not None:
        params['back'] = validate_back(back)

    return get_csv(get_content(NEAREST_HOTSPOTS_URL, params))


def list_regions(rtype, code=None):
    """List all regions.

    Fetch all the areas of type bcr, country, subnational1 or subnational2.
    The code argument is used to limit the records to a given country or
    subnational1 region.

    This maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-LocationReference

    :param rtype: the type of region to search for, 'bcr', 'country',
    'subnational1' or 'subnational2'.

    :param code: the region to limit the records returned.

    :return: the list of regions.

    :raises ValueError: if an invalid region type is given or if the code
    used to limit the scope of the search is for a region type that is narrower
    in focus that the region type argument.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {'rtype': validate_region_type(rtype)}

    if code:
        search_type = region_type_for_code(code)

        if params['rtype'] == 'bcr':
            raise ValueError("A country or subnational code cannot be used "
                             "with the region type 'bcr'.")

        if params['rtype'] == 'country':
            raise ValueError("A country or subnational code cannot be used "
                             "with the region type 'country'.")

        if params['rtype'] == 'subnational1' and search_type == 'subnational1':
            raise ValueError("A subnational1 code cannot be used with the "
                             "region type 'subnational1'.")

        if params['rtype'] == 'subnational1' and search_type == 'subnational2':
            raise ValueError("A subnational2 code cannot be used with the "
                             "region type 'subnational1'.")

        if params['rtype'] == 'subnational2' and search_type == 'subnational2':
            raise ValueError("A subnational2 code cannot be used with the "
                             "region type 'subnational2'.")

        params[search_type + 'Code'] = code

    return get_csv(get_content(LIST_REGIONS_URL, params))


def find_regions(rtype, match):
    """Find matching regions.

    Find all the areas of type bcr, country, subnational1 or subnational2
    which have a name that optionally matches a given keyword (partial or
    full, match case insensitive). If a keyword is not given then the full
    list is returned.

    This maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-LocationReference

    :param rtype: the type of region to search for, 'bcr', 'country',
    'subnational1' or 'subnational2'.

    :param match: keyword to find matching names.

    :return: the list of regions.

    :raises ValueError: if an invalid region type is given or if match is an
    empty string.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    if not match:
        raise ValueError("You specify a word to search for regions.")

    params = {
        'rtype': validate_region_type(rtype),
        'match': match,
    }
    return get_csv(get_content(FIND_REGIONS_URL, params))


def list_species(category='species', locale='en_US'):
    """Get the list of species in the eBird taxonomy.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-SpeciesReference

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species', 'spuh'. More
    than one value can be given in a comma-separated string.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :return: the list of species matching the species category.

    :raises ValueError: if an invalid category or locale is given.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        'cat': validate_category(category),
        'locale': validate_locale(locale),
    }

    return get_csv(get_content(LIST_SPECIES_URL, filter_parameters(params)))
