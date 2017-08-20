"""
Definitions of the arguments used in the command line scripts.

Since the scripts are just simple wrappers for the API calls and
in general the calls accepts the same general set of arguments the
definitions for each argument are created as dicts which are then
unpacked in the respective scripts.

"""

import click

from ebird.api.scripts import validation


BACK = {
    'type': int,
    'default': 14,
    'callback': validation.validate_back,
    'help': 'Fetch only hotspots visited within the past n days, where n is in the range 1..30.',
}

CATEGORY = {
    'default': 'species',
    'callback': validation.validate_category,
    'help': 'The category of species which may be one or more of:'
            ' domestic, form, hybrid, intergrade, issf, slash, species or spuh.',
}

CODE = {
    'prompt': True,
    'callback': validation.validate_code,
    'help': 'The code for a country, subnational1 or subnational2 area.'
}

CODE_OPTIONAL = {
    'default': None,
    'callback': validation.validate_code,
    'help': 'The code for a country, subnational1 or subnational2 area.'
}

CODES = {
    'multiple': True,
    'callback': validation.validate_codes,
    'help': 'The unique identifiers for up to 10 hotspots.'
}

DETAIL = {
    'type': click.Choice(['simple', 'full']),
    'default': 'simple',
    'help': "Return record in the 'simple' or 'full' format."
}

DIST = {
    'type': int,
    'default': 25,
    'callback': validation.validate_dist,
    'help': 'Fetch only hotspots within n kilometers, where n is in the range 0..50.',
}

HOTSPOT = {
    'is_flag': True,
    'default': False,
    'help': 'Only return observations from hotspots.',
}

INDENT = {
    'default': None,
    'type': int,
    'help': 'pretty-print the results with this level of indentation.'
}

LATITUDE = {
    'prompt': True,
    'type': float,
    'callback': validation.validate_lat,
    'help': "The latitude of the location.",
}

LOCALE = {
    'default': 'en_US',
    'callback': validation.validate_locale,
    'help': 'Limit the species to a give country and language.',
}

LONGITUDE = {
    'prompt': True,
    'type': float,
    'callback': validation.validate_lng,
    'help': "The longitude of the location.",
}

MATCH = {
    'prompt': True,
    'help': 'Return only regions that match this name. The match is case-sensitive.'
}

MAX_RESULTS = {
    'type': int,
    'default': None,
    'callback': validation.validate_max_results,
    'help': 'Limit the number of results returned from 1..10000. The default is to return all results.'
}

OUT = {
    'prompt': True,
    'type': click.File('wb'),
    'help': 'The name of a file to write the results to. To print the results to the screen use -.'
}

PROVISIONAL = {
    'is_flag': True,
    'default': False,
    'help': 'Include unverified records.',
}

REGION_TYPE = {
    'prompt': True,
    'callback': validation.validate_region_type,
    'help': "The region type. Must one of bcr, country, subnational1 or subnational2"
}

SPECIES = {
    'prompt': True,
    'help': "The species' scientific name."
}
