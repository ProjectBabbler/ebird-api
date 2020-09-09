# pylint: disable=C0111

"""Functions for validation."""

import re

from datetime import date, datetime
from enum import Enum

from ebird.api import constants

_locales = constants.LOCALES.values()
_region_types = ', '.join(constants.REGION_TYPES)
_sort_list = ', '.join(constants.SPECIES_SORT)
_species_categories = ', '.join(constants.SPECIES_CATEGORIES)
_species_ordering = ', '.join(constants.SPECIES_ORDERING)
_top_100_rank = ', '.join(constants.TOP_100_RANK)


class Transform(Enum):
    NONE = 1
    LOWER = 2
    UPPER = 3


def is_country(value):
    return re.match(r'^\w{2}$', value)


def is_subnational1(value):
    return re.match(r'^\w{2}-\w{1,}$', value)


def is_subnational2(value):
    return re.match(r'^\w{2}-\w{1,}-\w{1,}$', value)


def is_region(value):
    return (
        re.match(r'^\w{2}$', value) or
        re.match(r'^\w{2}-\w{1,}$', value) or
        re.match(r'^\w{2}-\w{1,}-\w{1,}$', value)
    )


def is_location(value):
    return re.match(r'^L\d+$', value.upper())


def get_location_type(value):
    if not value or not isinstance(value, str):
        raise ValueError('Location type must be a string.')
    if is_country(value):
        result = 'country'
    elif is_subnational1(value):
        result = 'subnational1'
    elif is_subnational2(value):
        result = 'subnational2'
    elif is_location(value):
        result = 'location'
    else:
        result = None
    return result


def get_location_types(items):
    results = set()
    for item in items:
        results.add(get_location_type(item))
    return list(results)


def clean_code(value, transform=Transform.NONE):
    if not value or not isinstance(value, str):
        raise ValueError('Code must be a string.')
    if transform == Transform.LOWER:
        value = value.lower()
    elif transform == Transform.UPPER:
        value = value.upper()
    return value.strip()


def clean_codes(value, transform=Transform.NONE):
    if isinstance(value, str):
        items = value.split(',')
    elif isinstance(value, list):
        items = value
    else:
        raise ValueError('Must be a comma-separated string or list of names')

    return [clean_code(code, transform=transform) for code in items]


def clean_lat(value):
    try:
        cleaned = float(value)
        if not -90 <= cleaned <= 90:
            raise ValueError()
        cleaned = "%.2f" % round(cleaned, 2)
    except ValueError as err:
        err.message = "Value for 'lat', %s, must be a decimal number" \
                      " in the range -90.00 to 90.00" % value
        raise

    return cleaned


def clean_lng(value):
    try:
        cleaned = float(value)
        if not -180 <= cleaned <= 180:
            raise ValueError()
        cleaned = "%.2f" % round(cleaned, 2)
    except ValueError as err:
        err.message = "Value for 'lon', %s, must be a decimal number" \
                      " in the range -180.00 to 180.00" % value
        raise

    return cleaned


def clean_dist(value):
    try:
        cleaned = int(value)
        if not 0 <= cleaned <= 50:
            raise ValueError()
    except ValueError as err:
        err.message = "Value for 'dist', %s is not an integer in the" \
                      " range 0..50" % value
        raise

    return cleaned


def clean_back(value):
    try:
        cleaned = int(value)
        if not 1 <= cleaned <= 30:
            raise ValueError()
    except ValueError as err:
        err.message = "Value for 'back', %s, is not an integer in the" \
                      " range 1..30" % value
        raise

    return cleaned


def clean_max_results(value, limit):
    try:
        cleaned = None if value is None else int(value)
        if cleaned is not None:
            if not 1 <= cleaned <= limit:
                raise ValueError()
    except ValueError as err:
        err.message = "Value for 'max_results', %s, is not None or an" \
                      " integer in the range 1..%d" % (value, limit)
        raise

    return cleaned


def clean_max_observations(value):
    return clean_max_results(value, 10000)


def clean_max_observers(value):
    return clean_max_results(value, 100)


def clean_max_checklists(value):
    return clean_max_results(value, 200)


def clean_locale(value):
    cleaned = str(value).strip()
    if re.match(r'^[a-zA-Z]{2}$', cleaned):
        cleaned = cleaned.lower()
    elif re.match(r'^[a-zA-Z]{2}_[a-zA-Z]{2,3}$', cleaned):
        cleaned = cleaned[:2].lower() + '_' + cleaned[3:].upper()

    if cleaned not in _locales:
        raise ValueError("eBird does not support this locale: %s" % cleaned)

    return cleaned


def clean_detail(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if cleaned not in ('simple', 'full'):
        raise ValueError(
            "Value for 'detail', %s, must be either 'simple' or 'full'" % value)
    return cleaned


def clean_provisional(value):
    return 'true' if bool(value) else 'false'


def clean_hotspot(value):
    return 'true' if bool(value) else 'false'


def clean_location(value):
    cleaned = clean_code(value, transform=Transform.UPPER)
    if not is_location(cleaned):
        raise ValueError('Invalid location identifier: %s' % cleaned)
    return cleaned


def clean_locations(values):
    cleaned = clean_codes(values, transform=Transform.UPPER)

    if len(cleaned) > 10:
        raise ValueError("List of locations cannot be longer than 10")

    for code in cleaned:
        if not is_location(code):
            raise ValueError("%s is not a location code" % code)

    return cleaned


def clean_region(value):
    cleaned = clean_code(value)
    if cleaned == 'WORLD':
        cleaned = cleaned.lower()
    elif cleaned != 'world':
        cleaned = cleaned.upper()
        if not is_region(cleaned):
            raise ValueError("Value for 'region', %s, must be a country, e.g. 'US',"
                             "subnational1, e.g. 'US-NV' or subnational2, e.g. 'US-NV-211'")
    return cleaned


def clean_region_type(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if cleaned not in constants.REGION_TYPES:
        raise ValueError(
            "Region type, %s, must be one or more of : %s" % (value, _region_types))
    return cleaned


def clean_area(value):
    cleaned = clean_code(value, transform=Transform.UPPER)
    area_type = get_location_type(cleaned)

    if area_type not in ['country', 'subnational1', 'subnational2', 'location']:
        raise ValueError('Unknown type of area: %s' % area_type)

    return cleaned


def clean_areas(values):
    cleaned = clean_codes(values, transform=Transform.UPPER)
    types = get_location_types(cleaned)

    if len(types) > 1:
        raise ValueError('You cannot mix different types of area together')
    else:
        if types[0] not in ['country', 'subnational1', 'subnational2', 'location']:
            raise ValueError('Unknown type of area')

    if len(cleaned) > 10:
        raise ValueError("List of areas cannot be longer than 10")

    return cleaned


def clean_categories(value):
    cleaned = clean_codes(value, transform=Transform.LOWER)
    for entry in cleaned:
        if entry not in constants.SPECIES_CATEGORIES:
            raise ValueError(
                "Species category, %s, must be one or more of : %s" % (
                    entry, _species_categories))
    return cleaned


def clean_ordering(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if cleaned not in constants.SPECIES_ORDERING:
        raise ValueError(
            "Species ordering, %s, must be one or more of : %s" % (value, _species_ordering))
    return cleaned


def clean_sort(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if cleaned not in constants.SPECIES_SORT:
        raise ValueError(
            "Species sort, %s, must be one or more of : %s" % (value, _sort_list))
    return cleaned


def clean_species_code(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if re.match(r'^\w{6}$', cleaned):
        return cleaned

    raise ValueError(
        "Value for 'species code', %s, must be 6 letters, e.g. 'cangoo'" % value)


def clean_date(value):
    if isinstance(value, str):
        cleaned = datetime.strptime(value, '%Y-%m-%d').date()
    elif isinstance(value, datetime):
        cleaned = value.date()
    elif isinstance(value, date):
        cleaned = value
    else:
        raise ValueError("Date must be a string ('YYYY-mm-dd'),"
                         " a date or a datetime: %s" % str(value))

    if cleaned.year < 1800:
        raise ValueError('Dates cannot be earlier than Jan 1st 1800')

    if cleaned > date.today():
        raise ValueError('Date is in the future: %s' % cleaned.strftime('%Y-%m-%d'))

    return cleaned.strftime('%Y/%m/%d')


def clean_rank(value):
    cleaned = clean_code(value, transform=Transform.LOWER)
    if cleaned not in constants.TOP_100_RANK:
        raise ValueError(
            "Top 100 rank, %s, must be one or more of : %s" % (value, _top_100_rank))
    return cleaned
