"""Functions for fetching information about the taxonomy used by eBird."""

from ebird.api.requests.utils import call
from ebird.api.requests.validation import (
    clean_categories,
    clean_codes,
    clean_locale,
    clean_ordering,
    clean_species_code,
)

TAXONOMY_URL = "https://api.ebird.org/v2/ref/taxonomy/ebird"
TAXONOMY_FORMS_URL = "https://api.ebird.org/v2/ref/taxon/forms/%s"
TAXONOMY_GROUPS_URL = "https://api.ebird.org/v2/ref/sppgroup/%s"
TAXONOMY_VERSIONS_URL = "https://api.ebird.org/v2/ref/taxonomy/versions"
TAXONOMY_LOCALES_URL = "https://api.ebird.org/v2/ref/taxa-locales/ebird"


def get_taxonomy(token, category=None, locale="en", version=None, species=None):
    """Get the full or specific subset of the taxonomy used by eBird.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#952a4310-536d-4ad1-8f3e-77cfb624d1bc

    :param token: the token needed to access the API.

    :param category: one or more categories of species to return: 'domestic',
    'form', 'hybrid', 'intergrade', 'issf', 'slash', 'species' or 'spuh'.
    More than one value can be given in a comma-separated string.

    :param locale: the language (to use) for the species common names. The
    default of 'en' will use species names from the eBird/Clements checklist.
    This can be any locale for which eBird has translations available. For a
    complete list see, http://help.ebird.org/customer/portal/articles/1596582.

    :param version: the version number of the taxonomy to return,
    see get_taxonomy_versions()

    :param species: a comma-separate string or list containing scientific
    names or 6-letter species codes.

    :return: the list of entries matching the category.

    :raises ValueError: if an invalid category or locale is given.

    :raises ValueError: if both a category and species are used. In this case
    the eBird API ignore the species and returns only results for the category.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    params = {"locale": clean_locale(locale), "fmt": "json"}

    if category is not None:
        params["cat"] = ",".join(clean_categories(category))

    if version is not None:
        params["version"] = version

    if species is not None:
        params["species"] = ",".join(clean_codes(species))

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(TAXONOMY_URL, params, headers)


def get_taxonomy_forms(token, species):
    """Get all the sub-specific forms of a given species.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#e338e5a6-919d-4603-a7db-6c690fa62371

    NOTE: the get_taxonomy() API call returns 6-letter species codes.

    :param token: the token needed to access the API.

    :param species: the 6-letter eBird species code, e.g. horlar (Horned Lark).

    :return: the list of codes of each sub-species.

    :raises ValueError is the species code is invalid (not 6 letters).

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TAXONOMY_FORMS_URL % clean_species_code(species)

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, {}, headers)


def get_taxonomy_groups(token, ordering="ebird", locale="en"):
    """Get the names of the groups of species used in the taxonomy.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#aa9804aa-dbf9-4a53-bbf4-48e214e4677a

    NOTE: Not all the locales supported by the eBird site or apps
    are available in the API. The following locales are not
    supported, (language, locale code):

    Croatian, hr
    Croatian, hr
    Faroese, fo
    Finnish, fi
    Haitian, ht_HT
    Hungarian, hu
    Indonesian, id
    Italian, it
    Japanese, ja
    Korean, ko
    Latvian, lv
    Lithuanian, lt
    Malayalam, ml
    Mongolian, mn
    Polish, pl
    Slovenian, sl
    Swedish, sv
    Ukrainian, uk

    :param token: the token needed to access the API.

    :param ordering: order groups using taxonomic order, 'ebird' or by
    likeness, 'merlin'.

    :param locale: the language (to use) for the group names.

    :return: the list of species groups.

    :raises ValueError: if an invalid ordering or locale is given.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    url = TAXONOMY_GROUPS_URL % clean_ordering(ordering)

    params = {
        "groupNameLocale": clean_locale(locale),
    }

    headers = {
        "X-eBirdApiToken": token,
    }

    return call(url, params, headers)


def get_taxonomy_versions(token):
    """Get all versions of the taxonomy, indicating which is the latest.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#9bba1ff5-6eb2-4f9a-91fd-e5ed34e51500

    :param token: the token needed to access the API.

    :return: a list of all the taxonomy versions used by eBird.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    headers = {
        "X-eBirdApiToken": token,
    }

    return call(TAXONOMY_VERSIONS_URL, {}, headers)


def get_taxonomy_locales(token):
    """Get all locales supported for common names.

    The maps to the end point in the eBird API 2.0,
    https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#3ea8ff71-c254-4811-9e80-b445a39302a6

    This API call returns a list of all the languages supported
    by eBird. An entry in the list takes the form:

        {'code': 'af', 'lastUpdate': '2024-12-21 06:06', 'name': 'Afrikaans'}

    There are currently, (2024-12-30), 107 languages available.

    :param token: the token needed to access the API.

    :return: a list of all the taxonomy locales used by eBird.

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    """
    headers = {
        "X-eBirdApiToken": token,
    }

    return call(TAXONOMY_LOCALES_URL, {}, headers)
