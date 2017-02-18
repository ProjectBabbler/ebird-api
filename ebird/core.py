# -*- coding: utf-8 -*-

"""Basic functions for accessing the eBird API.

    geo_observations() - get nearby recent observations.
    geo_species() - get nearby, recent observations of a species.
    geo_notable() - get nearby, recent observations of rare species.

    hotspot_observations() - get recent observations from a list of hotspots.
    hotspot_species() - get recent observations of a species from a list of hotspots.
    hotspot_notable() - get recent observations of a rare species from a list of hotspots.

    location_observations() - get recent observations from a list of locations.
    location_species() - get recent observations of a species from a list of locations.
    location_notable() - get recent observations of a rare species from a list of locations.

    region_observations() - get recent observations for a region.
    region_species() - get recent observations for s given species in a region.
    region_notable() - get recent observations of a rare species for a region.

    nearest_species() - the recent observations of a species from nearby locations.

    list_locations() - get the codes for countries, subnational1 or subnational2 areas.
    find_locations() - find countries, subnational1 or subnational2 areas that match a name.

"""
import csv
import json

from ebird.utils import region_type_for_code

try:
    import urllib.request as urlrequest
    from urllib.parse import urlencode
except ImportError:
    import urllib as urlrequest
    from urllib import urlencode

from ebird.validation import validate_lat, validate_lng, validate_dist, \
    validate_back, validate_max_results, validate_locale, validate_detail, \
    validate_provisional, validate_hotspot, validate_locations, validate_region, validate_region_type

GEO_OBSERVATIONS_URL = 'http://ebird.org/ws1.1/data/obs/geo/recent'
GEO_SPECIES_URL = 'http://ebird.org/ws1.1/data/obs/geo_spp/recent'
GEO_NOTABLE_URL = 'http://ebird.org/ws1.1/data/notable/geo/recent'

HOTSPOT_OBSERVATIONS_URL = 'http://ebird.org/ws1.1/data/obs/hotspot/recent'
HOTSPOT_SPECIES_URL = 'http://ebird.org/ws1.1/data/obs/hotspot_spp/recent'
HOTSPOT_NOTABLE_URL = 'http://ebird.org/ws1.1/data/notable/hotspot/recent'

LOCATION_OBSERVATIONS_URL = 'http://ebird.org/ws1.1/data/obs/loc/recent'
LOCATION_SPECIES_URL = 'http://ebird.org/ws1.1/data/obs/loc_spp/recent'
LOCATION_NOTABLE_URL = 'http://ebird.org/ws1.1/data/notable/loc/recent'

REGION_OBSERVATIONS_URL = 'http://ebird.org/ws1.1/data/obs/region/recent'
REGION_SPECIES_URL = 'http://ebird.org/ws1.1/data/obs/region_spp/recent'
REGION_NOTABLE_URL = 'http://ebird.org/ws1.1/data/notable/region/recent'

NEAREST_SPECIES_URL = 'http://ebird.org/ws1.1/data/nearest/geo_spp/recent'

LIST_LOCATIONS_URL = 'http://ebird.org/ws1.1/ref/location/list'
FIND_LOCATIONS_URL = 'http://ebird.org/ws1.1/ref/location/find'

# default values for the arguments passed the core functions.

OBSERVATION_DEFAULTS = {
    'back': 14,
    'dist': 25,
    'maxResults': None,
    'hotspot': 'false',
    'includeProvisional': 'false',
    'locale': 'en_US',
    'fmt': 'xml',
    'detail': 'simple',
}


def get_json(response):
    """Decode the JSON records from the response.

    :param response:
    :type response

    :return: the records decoded from the JSON payload.
    :rtype: list

    """
    return json.loads(response.read().decode('utf-8'))


def get_observations(url, params):
    """Get the observations from the eBird API.

    :param url: the URL for the API call.
    :typw url: str

    :param params: the query parameters for the API call
    :type params: dict

    :return: the decoded data
    :rtype: list

    """
    return get_json(urlrequest.urlopen(url + '?' + urlencode(params, doseq=True)))


def filter_parameters(params):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    result = {}
    for key, value in params.items():
        if key in OBSERVATION_DEFAULTS:
            if value != OBSERVATION_DEFAULTS[key]:
                result[key] = value
        else:
            result[key] = value

    return result


def geo_observations(lat, lng, dist=25, back=14, max_results=None,
                     locale='en_US', provisional=False, hotspot=False):
    """Get nearby recent observations of each species.

    Get recent observations (up to 30 days ago) of each species from all
    locations in an area centered on a set of coordinates (latitude,
    longitude) and optional distance (up to 50km away, with a default
    distance of 25km).

    NOTE: Only the most recent record of each species is returned.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNearbyObservations

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

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

    :param hotspot: get only observations from hotspots, in other words exclude
    private locations. The default is False so observations will be returned from
    all locations.

    :return: the list of observations in 'simple' form. See the eBird API
    documentation for a description of the fields.

    """
    params = {
        'lat': validate_lat(lat),
        'lng': validate_lng(lng),
        'dist': validate_dist(dist),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'hotspot': validate_hotspot(hotspot),
        'fmt': 'json',
    }

    return get_observations(
        GEO_OBSERVATIONS_URL, filter_parameters(params))


def geo_species(species, lat, lng, dist=25, back=14, max_results=None,
                locale='en_US', provisional=False, hotspot=False):
    """Get most recent observation of a species nearby.

    Get the most recent observation (up to 30 days ago) for a species seen at
    any locations in an area centered on a set of coordinates (latitude,
    longitude) and optional distance (up to 50km away).

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNearbyObservationsOfASpecies

    :param species: the scientific name of the species.

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

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

    :param hotspot: get only observations from hotspots, in other words exclude
    private locations. The default is False so observations will be returned from
    all locations.

    :return: the list of observations in 'simple' form. See the eBird API
    documentation for a description of the fields.

    """
    params = {
        'sci': species,
        'lat': validate_lat(lat),
        'lng': validate_lng(lng),
        'dist': validate_dist(dist),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'hotspot': validate_hotspot(hotspot),
        'fmt': 'json',
    }

    return get_observations(
        GEO_SPECIES_URL, filter_parameters(params))


def geo_notable(lat, lng, dist=25, back=14, max_results=None, locale='en_US',
                hotspot=False, detail='simple'):
    """Get the nearby, recent observations of rare species.

    Get all the recent observations (up to 30 days ago) for a species seen at
    locations in an area centered on a set of coordinates (latitude, longitude)
    and optional distance (up to 50km away) which are locally or nationally
    rare.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNearbyNotableObservations

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param hotspot: get only observations from hotspots, in other words exclude
    private locations. The default is False so observations will be returned from
    all locations.

    :param detail: return records in 'simple' or 'full' format. See the eBird API
    documentation for a description of the fields.

    :return: the list of observations.

    """
    params = {
        'lat': validate_lat(lat),
        'lng': validate_lng(lng),
        'dist': validate_dist(dist),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'hotspot': validate_hotspot(hotspot),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        GEO_NOTABLE_URL, filter_parameters(params))


def hotspot_observations(codes, back=14, max_results=None, locale='en_US',
                         provisional=False, detail='simple'):
    """Get recent observations from a list of hotspots.

    Get all the recent observations (up to 30 days ago) from up to 10
    hotspots.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsAtHotspots

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

    return get_observations(
        HOTSPOT_OBSERVATIONS_URL, filter_parameters(params))


def hotspot_species(species, codes, back=14, max_results=None, locale='en_US',
                    provisional=False, detail='simple'):
    """Get recent observations of a species from a list of hotspots.

    Get all the recent observations (up to 30 days ago) of a given species
    from up to 10 hotspots.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsOfASpeciesAtHotspots

    :param species: the scientific name of the species.

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

    """
    params = {
        'sci': species,
        'r': validate_locations(codes),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        HOTSPOT_SPECIES_URL, filter_parameters(params))


def hotspot_notable(codes, back=14, max_results=None, locale='en_US', detail='simple'):
    """Get recent observations of a rare species from a list of hotspots.

    Get all the recent observations (up to 30 days ago) of species classes
    as rare (locally or nationally) from up to 10 hotspots.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNotableObservationsAtHotspots

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

    :param detail: return records in 'simple' or 'full' format. See the eBird API
    documentation for a description of the fields.

    :return: the list of observations.

    """
    params = {
        'r': validate_locations(codes),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        HOTSPOT_NOTABLE_URL, filter_parameters(params))


def location_observations(codes, back=14, max_results=None, locale='en_US',
                          provisional=False, detail='simple'):
    """Get recent observations from a list of locations.

    Get all the recent observations (up to 30 days ago) from up to 10
    locations - hotspots and private.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsAtLocations

    :param codes: the unique identifiers, eg. L3733278 of up to 10 locations.

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

    return get_observations(
        LOCATION_OBSERVATIONS_URL, filter_parameters(params))


def location_species(species, codes, back=14, max_results=None, locale='en_US',
                     provisional=False, detail='simple'):
    """Get recent observations of a species from a list of locations.

    Get all the recent observations (up to 30 days ago) of a given species
    from up to 10 locations - hotspots and private.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsOfASpeciesAtLocations

    :param species: the scientific name of the species.

    :param codes: the unique identifiers, eg. L3733278 of up to 10 locations.

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

    """
    params = {
        'sci': species,
        'r': validate_locations(codes),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        LOCATION_SPECIES_URL, filter_parameters(params))


def location_notable(codes, back=14, max_results=None, locale='en_US', detail='simple'):
    """Get recent observations of a rare species from a list of locations.

    Get all the recent observations (up to 30 days ago) of species classes
    as rare (locally or nationally) from up to 10 locations - hotspots and
    private.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNotableObservationsAtLocations

    :param codes: the unique identifiers, eg. L3733278 of up to 10 locations.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param detail: return records in 'simple' or 'full' format. See the eBird API
    documentation for a description of the fields.

    :return: the list of observations.

    """
    params = {
        'r': validate_locations(codes),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        LOCATION_NOTABLE_URL, filter_parameters(params))


def region_observations(code, back=14, max_results=None, locale='en_US',
                        provisional=False, hotspot=False):
    """Get recent observations for a region.

    Get all the recent observations (up to 30 days ago) for a region.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsInARegion

    :param code: the code for the region, eg. US-NV.

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

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :return: the list of observations in simple format.

    """
    params = {
        'r': validate_region(code),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'hotspot': validate_hotspot(hotspot),
        'fmt': 'json',
    }

    return get_observations(
        REGION_OBSERVATIONS_URL, filter_parameters(params))


def region_species(species, code, back=14, max_results=None, locale='en_US',
                   provisional=False, hotspot=False):
    """Get recent observations for s given species in a region.

    Get all the recent observations (up to 30 days ago) for a species
    in a given region.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentObservationsOfASpeciesInARegion

    :param species: the scientific name of the species.

    :param code: the code for the region, eg. US-NV.

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

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :return: the list of observations in simple format.

    """
    params = {
        'sci': species,
        'r': validate_region(code),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'hotspot': validate_hotspot(hotspot),
        'fmt': 'json',
    }

    return get_observations(
        REGION_SPECIES_URL, filter_parameters(params))


def region_notable(code, back=14, max_results=None, locale='en_US',
                   hotspot=False, detail='simple'):
    """Get recent observations of a rare species for a region.

    Get all the recent observations (up to 30 days ago) of species classes
    as rare (locally or nationally) from up to 10 locations - hotspots and
    private.

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNotableObservationsAtLocations

    :param code: the code for the region, eg. US-NV.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :param detail: return records in 'simple' or 'full' format. See the eBird API
    documentation for a description of the fields.

    :return: the list of observations.

    """
    params = {
        'r': validate_region(code),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 10000),
        'locale': validate_locale(locale),
        'hotspot': validate_hotspot(hotspot),
        'detail': validate_detail(detail),
        'fmt': 'json',
    }

    return get_observations(
        REGION_NOTABLE_URL, filter_parameters(params))


def nearest_species(species, lat, lng, back=14, max_results=None,
                    locale='en_US', provisional=False, hotspot=False):
    """Get the nearest, recent, observations of a species.

    Get the recent observations (up to 30 days ago) for a species seen at
    locations closest to a set of coordinates (latitude, longitude).

    The maps to the end point in the eBird API 1.1,
    https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-NearestLocationsWithObservationsOfASpecies

    :param species: the scientific name of the species.

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 1000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en_US' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param provisional: include records which have not yet been reviewed.
    Either True or False, the default is False.

    :param hotspot: get only observations from hotspots, in other words exclude
    private locations. The default is False so observations will be returned from
    all locations.

    :return: the list of observations in 'simple' form. See the eBird API
    documentation for a description of the fields.

    """
    params = {
        'sci': species,
        'lat': validate_lat(lat),
        'lng': validate_lng(lng),
        'back': validate_back(back),
        'maxResults': validate_max_results(max_results, 1000),
        'locale': validate_locale(locale),
        'includeProvisional': validate_provisional(provisional),
        'hotspot': validate_hotspot(hotspot),
        'fmt': 'json',
    }

    return get_observations(
        NEAREST_SPECIES_URL, filter_parameters(params))


def get_csv(response):
    """Decode the CSV records from the response.

    :param response:
    :type response

    :return: the records decoded from the CSV payload.
    :rtype: list

    """
    content = response.read().decode('utf-8')
    return list(csv.DictReader(content.splitlines(), delimiter=','))


def get_locations(url, params):
    """Get the locations from the eBird API.

    :param url: the URL for the API call.
    :typw url: str

    :param params: the query parameters for the API call
    :type params: dict

    :return: the decoded data
    :rtype: list

    """
    return get_csv(urlrequest.urlopen(url + '?' + urlencode(params, doseq=True)))


def list_locations(rtype, code=None):
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

    return get_locations(LIST_LOCATIONS_URL, params)


def find_locations(rtype, match):
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

    """
    if not match:
        raise ValueError("You specify a word to search for regions.")

    params = {
        'rtype': validate_region_type(rtype),
        'match': match,
    }
    return get_locations(FIND_LOCATIONS_URL, params)
