# pylint: disable=R0913,R0914

"""Functions for fetching information about what species have been seen."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import (
    clean_areas,
    clean_back,
    clean_categories,
    clean_detail,
    clean_dist,
    clean_hotspot,
    clean_lat,
    clean_lng,
    clean_locale,
    clean_max_observations,
    clean_provisional,
    clean_sort,
)

OBSERVATIONS_URL = "https://api.ebird.org/v2/data/obs/%s/recent"
NOTABLE_OBSERVATIONS_URL = "https://api.ebird.org/v2/data/obs/%s/recent/notable"
SPECIES_OBSERVATIONS_URL = "https://api.ebird.org/v2/data/obs/%s/recent/%s"

NEARBY_OBSERVATIONS_URL = "https://api.ebird.org/v2/data/obs/geo/recent"
NEARBY_NOTABLE_URL = "https://api.ebird.org/v2/data/obs/geo/recent/notable"
NEARBY_SPECIES_URL = "https://api.ebird.org/v2/data/obs/geo/recent/%s"


NEAREST_SPECIES_URL = "https://api.ebird.org/v2/data/nearest/geo/recent/%s"

HISTORIC_OBSERVATIONS_URL = "https://api.ebird.org/v2/data/obs/%s/historic/%s"


def get_observations(
    token,
    area,
    back=14,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
    detail="simple",
    category=None,
):
    """Get recent observations (up to 30 days ago) for a region or location.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#3d2a17c1-2129-475c-b4c8-7d362d6000cd

    :param token: the token needed to access the API.

    :param area: a country, subnational1, subnational2 or location code
    or a list of up to 10 codes. All codes must be same type.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param provisional: include records which have not yet been reviewed.
    Either True or False, the default is False.

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :param detail: return records in 'simple' or 'full' format. See the eBird
    API documentation for a description of the fields.

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string. The default
    value is None and records from all categories will be returned.

    :return: the list of observations in simple format.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """

    cleaned = clean_areas(area)

    url = OBSERVATIONS_URL % cleaned[0]

    params = {
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
        "detail": clean_detail(detail),
    }

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    if len(cleaned) > 1:
        params["r"] = ",".join(cleaned)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_notable_observations(
    token, area, back=14, max_results=None, locale="en", hotspot=False, detail="simple"
):
    """Get recent observations of a rare species for a region or location

    Get all the recent observations (up to 30 days ago) of species classes
    as rare (locally or nationally) for a country, subnational1 region,
    subnational2 region or location.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#397b9b8c-4ab9-4136-baae-3ffa4e5b26e4

    :param token: the token needed to access the API.

    :param area: a country, subnational1, subnational2 or location code
    or a list of up to 10 codes. All codes must be same type.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :param detail: return records in 'simple' or 'full' format. See the eBird
    API documentation for a description of the fields.

    :return: the list of observations.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    cleaned = clean_areas(area)

    url = NOTABLE_OBSERVATIONS_URL % cleaned[0]

    params = {
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "hotspot": clean_hotspot(hotspot),
        "detail": clean_detail(detail),
    }

    if len(cleaned) > 1:
        params["r"] = ",".join(cleaned)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_species_observations(
    token,
    species,
    area,
    back=14,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
    detail="simple",
    category=None,
):
    """Get recent observations for a given species in a region.

    Get all the recent observations (up to 30 days ago) for a species
    in a given region.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#755ce9ab-dc27-4cfc-953f-c69fb0f282d9

    :param token: the token needed to access the API.

    :param species: the scientific name of the species.

    :param area: a country, subnational1, subnational2 or location code
    or a list of up to 10 codes. All codes must be same type.

    :param back: the number of days in the past to include. Ranges from
    1 to 30 with a default of 14 days.

    :param max_results: the maximum number of observations to return from
    1 to 10000. The default value is None which means all observations will
    be returned.

    :param locale: the language (to use) for the species common names. The
    default of 'en' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param provisional: include records which have not yet been reviewed.
    Either True or False, the default is False.

    :param hotspot: return records only from hotspots, True or include both
    hotspots and private locations, False (the default).

    :param detail: return records in 'simple' or 'full' format. See the eBird
    API documentation for a description of the fields.

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string. The default
    value is None and records from all categories will be returned. It's not clear
    what the purpose of this parameter is given the species is being specified.
    It is not documented on the eBird API page but it is supported by the code.

    :return: the list of observations in simple format.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    cleaned = clean_areas(area)

    url = SPECIES_OBSERVATIONS_URL % (cleaned[0], species)

    params = {
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
        "detail": clean_detail(detail),
    }

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    if len(cleaned) > 1:
        params["r"] = ",".join(cleaned)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_nearby_observations(
    token,
    lat,
    lng,
    dist=25,
    back=14,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
    category=None,
    sort="date",
):
    """Get nearby recent observations of each species.

    Get recent observations (up to 30 days ago) of each species from all
    locations in an area centered on a set of coordinates (latitude,
    longitude) and optional distance (up to 50km away, with a default
    distance of 25km).

    NOTE: Only the most recent record of each species is returned.

    The maps to the end point in the eBird API 1.1,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#62b5ffb3-006e-4e8a-8e50-21d90d036edc

    :param token: the token needed to access the API.

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

    :param hotspot: get only observations from hotspots, in other words
    exclude private locations. The default is False so observations will
    be returned from all locations.

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string. The default
    value is None and records from all categories will be returned.

    :param sort: return the records sorted by date, 'date' or taxonomy, 'species'.

    :return: the list of observations in simple format.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        "lat": clean_lat(lat),
        "lng": clean_lng(lng),
        "dist": clean_dist(dist),
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
        "sort": clean_sort(sort),
    }

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(NEARBY_OBSERVATIONS_URL, params, headers)


def get_nearby_species(
    token,
    species,
    lat,
    lng,
    dist=25,
    back=14,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
    category=None,
):
    """Get most recent observation of a species nearby.

    Get the most recent observation (up to 30 days ago) for a species seen at
    any locations in an area centered on a set of coordinates (latitude,
    longitude) and optional distance (up to 50km away).

    The maps to the end point in the eBird API 1.1,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#20fb2c3b-ee7f-49ae-a912-9c3f16a40397

    :param token: the token needed to access the API.

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

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string. The default
    value is None and records from all categories will be returned. It's not
    clear what the purpose of this parameter is given the species is being
    specified. It is not documented on the eBird API page but it is supported
    by the code.

    :return: the list of observations in 'simple' form. See the eBird API
    documentation for a description of the fields.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = NEARBY_SPECIES_URL % species

    params = {
        "lat": clean_lat(lat),
        "lng": clean_lng(lng),
        "dist": clean_dist(dist),
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
    }

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_nearby_notable(
    token,
    lat,
    lng,
    dist=25,
    back=14,
    max_results=None,
    locale="en",
    hotspot=False,
    detail="simple",
):
    """Get the nearby, recent observations of rare species.

    Get all the recent observations (up to 30 days ago) for a species seen at
    locations in an area centered on a set of coordinates (latitude, longitude)
    and optional distance (up to 50km away) which are locally or nationally
    rare.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#caa348bb-71f6-471c-b203-9e1643377cbc

    :param token: the token needed to access the API.

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

    :param hotspot: get only observations from hotspots, in other words
    exclude private locations. The default is False so observations will be
    returned from all locations.

    :param detail: return records in 'simple' or 'full' format. See the eBird
    API documentation for a description of the fields.

    :return: the list of observations.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {
        "lat": clean_lat(lat),
        "lng": clean_lng(lng),
        "dist": clean_dist(dist),
        "back": clean_back(back),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "hotspot": clean_hotspot(hotspot),
        "detail": clean_detail(detail),
    }

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(NEARBY_NOTABLE_URL, params, headers)


def get_nearest_species(
    token,
    species,
    lat,
    lng,
    dist=25,
    back=14,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
):
    """Get the nearest, recent, observations of a species.

    Get the recent observations (up to 30 days ago) for a species seen at
    locations closest to a set of coordinates (latitude, longitude).

    IMPORTANT: As of 2019-05-27 the dist parameter does not appear to be
    respected and so this call will return records from anywhere the
    specified species are reported. Also the English common name for the
    species is always returned regardless of which locale is specified.

    The maps to the end point in the eBird API 1.1,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#6bded97f-9997-477f-ab2f-94f254954ccb

    :param token: the token needed to access the API.

    :param species: the scientific name of the species.

    :param lat: the latitude, which will be rounded to 2 decimal places.

    :param lng: the longitude, which will be rounded to 2 decimal places.

    :param dist: include all sites within this distance, from 0 to 50km
    with a default of 25km.

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

    :param hotspot: get only observations from hotspots, in other words
    exclude private locations. The default is False so observations will
    be returned from all locations.

    :return: the list of observations in 'simple' form. See the eBird API
    documentation for a description of the fields.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = NEAREST_SPECIES_URL % species

    params = {
        "lat": clean_lat(lat),
        "lng": clean_lng(lng),
        "back": clean_back(back),
        "dist": clean_dist(dist),
        "maxObservations": clean_max_observations(max_results),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
    }

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_historic_observations(
    token,
    area,
    date,
    max_results=None,
    locale="en",
    provisional=False,
    hotspot=False,
    detail="simple",
    category=None,
):
    """Get recent observations for a region.

    Get all the recent observations (up to 30 days ago) for a region.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#2d8c6ee8-c435-4e91-9f66-6d3eeb09edd2

    :param token: the token needed to access the API.

    :param area: a country, subnational1, subnational2 or location code
    or a list of up to 10 codes. All codes must be same type.

    :param date: the date, since Jan 1st 1800.

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

    :param detail: return records in 'simple' or 'full' format. See the
    eBird API documentation for a description of the fields.

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string. The default
    value is None and records from all categories will be returned.

    :return: the list of observations in simple format.

    :raises ValueError: if any of the arguments fail the validation checks.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    cleaned = clean_areas(area)

    url = HISTORIC_OBSERVATIONS_URL % (cleaned[0], date.strftime("%Y/%m/%d"))

    params = {
        "rank": "mrec",
        "detail": clean_detail(detail),
        "sppLocale": clean_locale(locale),
        "includeProvisional": clean_provisional(provisional),
        "hotspot": clean_hotspot(hotspot),
        "maxObservations": clean_max_observations(max_results),
    }

    if len(cleaned) > 1:
        params["r"] = ",".join(cleaned)

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)
