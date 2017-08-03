[![Build Status](https://travis-ci.org/ProjectBabbler/ebird-api.svg?branch=master)](https://travis-ci.org/ProjectBabbler/ebird-api)
[![PyPI version](https://badge.fury.io/py/ebird-api.svg)](https://badge.fury.io/py/ebird-api)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/ebird-api.svg)](https://img.shields.io/pypi/pyversions/ebird-api)

# eBird API

eBird API provides a set of wrapper functions for accessing the end-points
in the eBird API.


## Install

```sh
pip install ebird-api
```

To install the earlier python 2.7 compatible version run:

```sh
pip install ebird-api==1.0.2
```

## Usage

Each of the core functions map to a specific end-point in the API. The 
end-points can be divided into three categories: fetching observations,
fetching the reference data (locations, species, etc.) used in the eBird
database and a single product end-point that works with Google Gadgets to
embed observation and visit information in web pages.

### Fetch Observations

Functions for fetching the records of what has been seen make up the 
bulk of the API. There are functions for fetching all the observations 
for hotspots and private locations; fetching all notable sightings of 
locally or nationally rare birds for a region or an area; fetching the 
latest sighting of each species in a region or area and finding the 
nearest location where a given species can be seen.

#### Fetching observations for a set of locations (private or hotspots):

```python
from ebird.api import location_observations, location_species, location_notable

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
```

#### Fetching observations for a set of hotspots:

```python
from ebird.api import hotspot_observations, hotspot_species, hotspot_notable

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
```

#### Fetching observations for a region:

```python
from ebird.api import region_observations, region_species, region_notable

# Get the most recent sightings of each species for Madison county, New 
# York for the past week.
records = region_observations('US-NY-053', back=7)

# Get all most recent sighting of Canada Goose in New York state within 
# the past two weeks.
records = region_species('Branta canadensis', 'US-NY')

# Get all the records of locally or nationally rare birds for New York
# county (including Central Park) for the past week.
records = region_notable('US-NY-061', back=7)
```

#### Fetching observations for an are (using a set of coordinates):

```python
from ebird.api import geo_observations, geo_species, geo_notable

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
```

#### Finding out where the nearest place to see a species:

```python
from ebird.api import nearest_species

# Where is the closest place to Cornell Lab of Ornithology to see
# Tennessee Warbler. Depending on when you try this you might have
# far to travel.
records = nearest_species('Oreothlypis peregrina', 42.48, -76.45)
```

### Reference data

The API also has functions for fetching the reference data (species, areas
and locations) used in the eBird database:

```python
from ebird.api import find_regions, list_regions, list_species, list_hotspots

# Get the list of states in the US.
states = list_regions('subnational1', 'US')

# Get the list of counties in New York state.
counties = list_regions('subnational2', 'US-NY')

# Find all the counties in the USA with 'west' in their name.
counties = find_regions('subnational2', 'west')

# List all the hotspots in New York state.
hotspots = list_hotspots('US-NY')

# List all the hotspots in New York state visited in the past week.
hotspots = list_hotspots('US-NY', back=7)

# Get all the species in the eBird taxonomy.
species = list_species()

# Get all the  identifiable sub-species and species with distinctive types
# of plumage.
species = list_species('issf,form')

```

### Product data

The product end-point is used by Google Gadgets (widgets) that can be 
added to a web site to show what species have been seen for a given 
location or area:

```python
from ebird.api import hotspot_summary

# Get a summary of the records at a hotspot for the past week.
records = hotspot_summary('L128530', back=7)

```

Each of these functions support arguments (with sensible defaults) for all
the query parameters supported by the eBird API. Check the docstring for
each function for more details. There you will also find a link to the
documentation for each end-point.

## Compatibility

ebird-api works with Python 3.3+. 

The previous version, 1.0.2, works with python 2.7, 3.3, 3.4, 3.5 and 3.6. It is 
feature complete and provides the same set of functions as the current release.

## Links

Documentation for the eBird API: https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

Available translations for species names: http://help.ebird.org/customer/portal/articles/1596582

Information on the taxonomy used by eBird: http://help.ebird.org/customer/portal/articles/1006825-the-ebird-taxonomy

## License

eBird API is available under the terms of the [MIT](https://opensource.org/licenses/MIT) licence.