# -*- coding: utf-8 -*-

"""Functions for cleaning and validating the parameters passed to the
eBird API:

    validate_lat() - verify the latitude in a pair of coordinates.
    validate_lon() - verify the longitude in a pair of coordinates.
    validate_dist() - verify the radius from a pair of coordinates.
    validate_back() - verify the number of days to fetch records for.
    validate_max_results() - verify the number of observations to fetch.
    validate_locale() - verify the locale used for species common names.
    validate_detail() - verify the detail records are returned in.
    validate_provisional - verify the flag used to include unverified records.
    validate_hotspot - verify the flag used to fetch records only from hotspots.
    validate_region - verify the code for a country, region or county.
    validate_location - verify the list of up to 10 location codes.

All functions returned a cleaned value that will be used in the call to
eBird API, e.g. boolean flags are converted to the strings 'true' or 'false'.
A ValueError is raised if the value(s) would cause the eBird API to return
an error - avoiding the cost of a network access.

"""

import re


def validate_lat(value):
    """Validate lat is coordinate in the range -90 to 90.

    :param value: the value to be validated.

    :returns: the cleaned, floating-point value.
    :rtype: str

    :raises ValueError if the value is not an decimal in the
    range -90.00 to 90.00 or has more than 2 decimal places
    of precision.

    """
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


def validate_lng(value):
    """Validate lng is coordinate in the range -180 to 180.

    The value will be rounded to 2 decimal places.

    :param value: the value to be validated.

    :returns: the cleaned, floating-point value.
    :rtype: str

    :raises ValueError if the value is not an decimal in the
    range -180.00 to 180.00.

    """
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


def validate_dist(value):
    """Validate dist is an integer in the range 0..50.

    :param value: the value to be validated.

    :returns: the cleaned, integer value.
    :rtype: int

    :raises ValueError if the value is not an integer in the range 0..50.

    """
    try:
        cleaned = int(value)
        if not 0 <= cleaned <= 50:
            raise ValueError()
    except ValueError as err:
        err.message = "Value for 'dist', %s is not an integer in the" \
                      " range 0..50" % value
        raise

    return cleaned


def validate_back(value):
    """Validate back is an integer in the range 1..30.

    :param value: the value to be validated.

    :returns: the cleaned, integer value.
    :rtype: int

    :raises ValueError if the value is not an integer in the range 1..30.

    """
    try:
        cleaned = int(value)
        if not 1 <= cleaned <= 30:
            raise ValueError()
    except ValueError as err:
        err.message = "Value for 'back', %s, is not an integer in the" \
                      " range 1..30" % value
        raise

    return cleaned


def validate_max_results(value, limit):
    """Validate max_results is none or an integer in a range.

    :param value: the value to be validated.

    :param limit: the maximum value for the max_results parameter.
    :type limit: int

    :returns: None or the integer value for the max results parameter.
    :rtype: None or int

    :raises ValueError if the value is not None or an integer in the
    range 1..10000.

    """
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


def validate_locale(value):
    """Validate locale is a valid language and optional country code.

    The locale used by the eBird API for the species common name is made
    up of a language code (ISO-639) and an optional country code (ISO-3166),
    for example 'es', 'de_DE'.

    This function does not attempt to verify that the locale is actually
    one supported by the eBird API.

    The case of hte string will be corrected: the language code will be
    converted to lower case and the country code to upper case.

    :param value: the value to be validated.
    :type value: str

    :returns: the cleaned string value for the locale.
    :rtype: str

    :raises ValueError if the value is not in the form xx_YY.

    """
    cleaned = str(value)
    if re.match(r'^[a-zA-Z]{2}$', cleaned):
        return cleaned.lower()
    elif re.match(r'^[a-zA-Z]{2}_[a-zA-Z]{2}$', cleaned):
        return cleaned[:2].lower() + '_' + cleaned[-2:].upper()
    else:
        raise ValueError("Invalid code for 'locale': %s" % value)


def validate_detail(value):
    """Validate the format observations should be returned in.

    The value will be converted to lower case before being validated.

    :param value: the value to be validated.
    :type value: str

    :returns: the cleaned, string value for the detail parameter.
    :rtype: str

    :raises ValueError if the format is not 'simple' or 'full'.

    """
    cleaned = str(value).lower()

    if cleaned != 'simple' and cleaned != 'full':
        raise ValueError(
            "Value for 'detail', %s, must be either 'simple' or 'full'" % value)

    return cleaned


def validate_provisional(value):
    """Validate whether provisional records should be included.

    :param value: the value to be validated.

    :returns: the string value, 'true' or 'false' for the provisional parameter.
    :rtype: str

    :raises ValueError if the value is not a boolean.

    """
    try:
        cleaned = bool(value)
    except ValueError as err:
        err.message = "Value for 'provisional', %s, must be a boolean" % value
        raise

    return 'true' if cleaned else 'false'


def validate_hotspot(value):
    """Validate whether records only from hotspots should be returned.

    :param value: the value to be validated.

    :returns: the string value, 'true' or 'false' for the hotspot parameter.
    :rtype: str

    :raises ValueError if the value is not a boolean.

    """
    try:
        cleaned = bool(value)
    except ValueError as err:
        err.message = "Value for 'hotspot', %s, must be a boolean" % value
        raise

    return 'true' if cleaned else 'false'


def validate_region(value):
    """Validate the region (country, subnational1 or subnational2) code.

    :param value: the value to be validated.
    :type value: str

    :return: the cleaned, region code.
    :rtype: str

    :raises: ValueError the code does not match the pattern for a country,
    region or county.

    """
    cleaned = value.upper()
    if re.match(r'^\w{2}$', cleaned):
        return cleaned
    elif re.match(r'^\w{2}-\w{2}$', cleaned):
        return cleaned
    elif re.match(r'^\w{2}-\w{2}-\w{2,}$', cleaned):
        return cleaned
    else:
        raise ValueError("Value for 'region', %s, must be a country, e.g. 'US',"
                         "region/state, e.g. 'US-NV' or county, e.g. 'US-NV-211'")


def validate_locations(values):
    """Validate the list of locations to fetch observations for.

    :param values: a list of location codes, e.g. L326536.

    :return: the list of validated codes.
    :rtype: list

    :raises ValueError if there are more than 10 locations in the list or if any
    of the codes do not match a location identifier.

    """
    if isinstance(values, str):
        values = [values]

    if len(values) > 10:
        raise ValueError("List of location codes cannot be longer than 10")

    for value in values:
        if not re.match(r'^L\d{1,}$', value):
            raise ValueError("Value for the location code, %s, must be the"
                             " letter 'L' followed by 1 or more digits." % value)

    return values[:]


def validate_region_type(value):
    """Validate the region type.

    :param value: the region type one of 'bcr', 'country', 'subnational1' or
    'subnational2'
    :type value: str

    :return the validated region type:
    :rtype: str

    :raises ValueError if the value is not a valida region type.

    """
    rtypes = ['bcr', 'country', 'subnational1', 'subnational2']

    cleaned = value.lower()
    if cleaned not in rtypes:
        raise ValueError(
            "Value for region type, %s, must be either: "
            "'bcr', 'country', 'subnational1' or 'subnational2'" % value)

    return cleaned


def validate_country(value):
    """Validate the country code.

    :param value: the value to be validated.
    :type value: str

    :return: the cleaned, country code.
    :rtype: str

    :raises: ValueError the code does not match the pattern for a country.

    """
    cleaned = value.upper()
    if re.match(r'^\w{2}$', cleaned):
        return cleaned
    else:
        raise ValueError(
            "Value for 'rtype', %s, must be a country code, e.g. 'US'" % value)


def validate_category(value):
    """Validate the species category or categories.

    :param value: the species category one of 'domestic', 'form', 'hybrid',
    'intergrade', 'issf', 'slash', 'species', 'spuh'. Multiple values can
    be given if they are separated by commas.

    :raises ValueError if the value is not one of the allowed categories.

    """
    categories = ['domestic', 'form', 'hybrid', 'intergrade', 'issf', 'slash',
                  'species', 'spuh']

    if ',' in value:
        cleaned = value.split(',')
    else:
        cleaned = [value.lower()]

    for category in cleaned:
        if category not in categories:
            raise ValueError(
                "Value for species category, %s, must be one or more of : "
                "'domestic', 'form', 'hybrid', 'intergrade', 'issf', "
                "'slash', 'species' or 'spuh'" % value)

    return ','.join(cleaned)
