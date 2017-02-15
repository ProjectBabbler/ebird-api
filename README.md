# eBird API

eBird API provides a set of wrapper functions for accessing the end-points
in the eBird API.

# Install

```sh
pip install ebird-api
```

## Usage

Each of the core functions map to a specific end-point:

```python
from ebird import \
    geo_observations, geo_species, geo_notable, \
    hotspot_observations, hotspot_species, hotspot_notable, \
    location_observations, location_species, location_notable, \
    region_observations, region_species, region_notable, \
    nearest_species

# Get the most recent sighting of the the first 100 species within 5km 
# of here in the past week. Coordinates will be rounded to 2 decimal places.
records = geo_observations(42.48, -76.45, dist=5, back=7, max_results=100)

# Get the most recent sighting of each species within 25km of here in 
# the past week but only from hotspots and with common names in Spanish.
records = geo_observations(
    42.48, -76.45, back=7, locale='es', provisional=True, hotspot=True)

# Get the most recent sighting of Canada Goose near here in the past 2 weeks.
records = geo_species('Branta canadensis', 42.48, -76.45)

# Get the latest sightings of local or nationally rare birds seen near here
# in the past 10 days. Return all the available fields for each record.
records = geo_notable(42.48, -76.45, back=10, detail='full')

# Codes for some of the main hotspots in Seattle, Washington.
hotspots = ['L128530', 'L351484', 'L162766', 'L269461', 'L571490']

# Get all the records of what has been seen in the past week. Only the
# basic set of fields ('simple' format) are returned.
records = hotspot_observations(hotspots, back=7)

# Get all the records for Canada Goose in the past 2 weeks. Include
# records that have not been reviewed and return all the fields available.
records = hotspot_species(
    'Branta canadensis', hotspots, provisional=True, detail='full')

# Get all the most sightings of locally or nationally rare birds for the past
# 30 days. Include all the fields available.
records = hotspot_notable(hotspots, back=30, detail='full')

# Code for the most visited locations in Madison county, New York:
# Woodman Pond, Ditch Bank Rd., Cornell Biological Field Station and
# Anne V Pickard Memorial Wildlife Overlook.
locations = ['L227544', 'L273783', 'L677871', 'L2313391']

# The functions for fetching records for locations are identical to
# those for hotspots. The only difference is you can include codes for
# any location, hotspot or private. Codes for private locations are
# ignored if you pass them to the hotspot functions.

records = location_observations(locations, back=7)

records = location_species(
    'Branta canadensis', locations, provisional=True, detail='full')

records = location_notable(locations, back=30, detail='full')

# Get the most recent sightings of each species for Madison county, New 
# York for the past week.
records = region_observations('US-NY-053', back=7)

# Get all most recent sighting of Canada Goose in New York state within 
# the past two weeks.
records = region_species('Branta canadensis', 'US-NY')

# Get all the records of locally or nationally rare birds for New York
# county (including Central Park) for the past week.
records = region_notable('US-NY-061', back=7)

# Where is the closest place to Cornell Lab of Ornithology to see
# Tennessee Warbler. Depending on when you try this you might have
# far to travel.
records = nearest_species('Oreothlypis peregrina', 42.48, -76.45)
```

Each of these functions support arguments (with sensible defaults) for all
the query parameters supported by the eBird API. Check the docstring for
each function for more details.

## Compatibility

ebird-api works with Python 2.7, 3.3, 3.4, 3.5, 3.6. It works with Python 2.6
but the tests use assertDictEqual() which were introduced only in Python 2.7.
It also works with Python 3.2 but tox which is used to run the tests does not.

## Resources

Documentation for the eBird API: https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

Available translations for species names: http://help.ebird.org/customer/portal/articles/1596582