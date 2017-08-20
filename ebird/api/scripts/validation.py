"""
Callback functions for validating script inputs.

"""

import click

from ebird.api import validation


# noinspection PyUnusedLocal
def validate_region_type(ctx, param, value):
    try:
        return validation.validate_region_type(value)
    except ValueError:
        raise click.BadParameter(
            'must be either bcr, country, subnational1 or subnational2.')


# noinspection PyUnusedLocal
def validate_dist(ctx, param, value):
    try:
        return validation.validate_dist(value)
    except ValueError:
        raise click.BadParameter('must be in the range 0..50.')


# noinspection PyUnusedLocal
def validate_back(ctx, param, value):
    try:
        return validation.validate_back(value)
    except ValueError:
        raise click.BadParameter('must be in the range 1..30.')


# noinspection PyUnusedLocal
def validate_code(ctx, param, value):
    try:
        if value is not None:
            return validation.validate_region(value)
    except ValueError:
        raise click.BadParameter(
            'must be a country, e.g. US, region/state, e.g. US-NV'
            ' or county, e.g. US-NV-211')


# noinspection PyUnusedLocal
def validate_codes(ctx, param, value):
    try:
        return validation.validate_locations(value)
    except ValueError:
        raise click.BadParameter(
            'invalid location or hotspot code.')


# noinspection PyUnusedLocal
def validate_lat(ctx, param, value):
    try:
        return validation.validate_lat(value)
    except ValueError:
        raise click.BadParameter('must be in the range -90.0..90.0')


# noinspection PyUnusedLocal
def validate_lng(ctx, param, value):
    try:
        return validation.validate_lng(value)
    except ValueError:
        raise click.BadParameter('must be in the range -180.0..180')


# noinspection PyUnusedLocal
def validate_category(ctx, param, value):
    try:
        return validation.validate_category(value)
    except ValueError:
        raise click.BadParameter('must be one of domestic, form, hybrid, '
                                 'intergrade, issf, slash, species or spuh')


# noinspection PyUnusedLocal
def validate_max_results(ctx, param, value):
    try:
        return validation.validate_max_results(value, 10000)
    except ValueError:
        raise click.BadParameter('must be in the range 1..10000.')


# noinspection PyUnusedLocal
def validate_locale(ctx, param, value):
    try:
        return validation.validate_locale(value)
    except ValueError:
        raise click.BadParameter('invalid code.')
