[![PyPI version](https://badge.fury.io/py/ebird-api.svg)](https://badge.fury.io/py/ebird-api)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/ebird-api.svg)](https://img.shields.io/pypi/pyversions/ebird-api)

# eBird API

eBird API Requests provides a set of wrapper functions for accessing the
end-points in the eBird API 2.0.

## Install

```sh
pip install ebird-api
```

## Usage

Each of the functions map to a specific end-point in the API - with one or
two exceptions where API calls are essentially identical. The functions can
be grouped into five activities: fetching observations, getting information
on hotspots, getting information on regions, getting lists of species and
getting statistics.

All functions support arguments (with sensible defaults) for all the query
parameters supported by the eBird API. Check the docstring for each function
for more details. There you will also find a link to the documentation for
each end-point.

To use the API you will need to register for an API key. All you need to do is
fill out this [form](https://ebird.org/api/keygen) and the API key is generated
automatically.

NOTE: Use the API with some restraint. Data costs money so don't go downloading
all the checklists for the world or other excessive behaviour or your account will
get banned. If you have a project in mind get in touch with eBird and tell them
what you want to do - they will be interested to hear it.

### Observations

```python
import os

from ebird.api.requests import get_observations

# Always store secrets outside the code, so you don't accidentally
# commit them. Environment variables are ideal for this.
api_key = os.environ["EBIRD_API_KEY"]

# Get observations from Woodman Pond, Madison county, New York for the past week.
this_week = get_observations(api_key, 'L227544', back=7)

# Get observations from Madison county, New York
country_records = get_observations(api_key, 'US-NY-053')

# Get observations from New York
state_records = get_observations(api_key, 'US-NY')

# Get observations from the USA - don't overdo the data downloads
national_records = get_observations(api_key, 'US')
```

Any where you pass in single location or region you can also pass in a
list or a comma-separated string. You can specify up to 10 locations or
regions:

```python
import os

from ebird.api.requests import get_observations

api_key = os.environ["EBIRD_API_KEY"]

# Get the observations for the most visited locations in Madison county, New York:
# Woodman Pond, Ditch Bank Rd., Cornell Biological Field Station and
# Anne V Pickard Memorial Wildlife Overlook.
locations = ['L227544', 'L273783', 'L677871', 'L2313391']
get_observations(api_key, locations, provisional=True, detail='full')

# Get the observations for Suffolk, Nassau and Queens counties in New York state.
counties = 'US-NY-103,US-NY-059,US-NY-81'
records = get_observations(api_key, locations, hotspot=False, category='species')
```

The common name for species can be returned in different languages by
specifying locale in the functions that return observations, checklists
or taxonomy:

```python
import os

from ebird.api.requests import get_observations

api_key = os.environ["EBIRD_API_KEY"]

records = get_observations(api_key, 'CA-QC', locale='fr')
```

In addition to getting all the observations for a given location or in
an area you can also get the latest observation of each species in a
geographical area - useful for finding the nearest place to see a given
species:

```python
import os

from ebird.api.requests import get_nearby_observations

api_key = os.environ["EBIRD_API_KEY"]

# Get the most recent sightings of all species seen in the last week within
# 10km of Point Reyes National Seashore.
records = get_nearby_observations(api_key, 38.05, -122.94, dist=10, back=7)
```

The calls to get_observations() and get_nearby_observation() return all the
available records. You can limit the set of records returned to only include
notable ones (locally or nationally rare species) or limit the records to
a small number of species:

```python
import os

from ebird.api.requests import (
    get_notable_observations,
    get_nearby_notable,
    get_species_observations,
    get_nearby_species,
)

api_key = os.environ["EBIRD_API_KEY"]

# Get the interesting birds seen in New York state.
notables = get_notable_observations(api_key, 'US-NY')

# Get the observations of Horned Lark (Eremophila alpestris) in New York state.
records = get_species_observations(api_key, 'horlar', 'US-NY')

# Get the interesting birds within 50kn of Point Reyes
nearby_notables = get_nearby_notable(api_key, 38.05, -122.94, dist=50)

# Find out if Barn Swallows have been seen in the area in the past 10 days
nearby_species = get_nearby_species(api_key, 'barswa', 38.05, -122.94, back=10)
```

For the more travel-minded you can also find out the nearest place to see a given species:

```python
import os

from ebird.api.requests import get_nearest_species

api_key = os.environ["EBIRD_API_KEY"]

# Where is the closest place to Cornell Lab of Ornithology to see
# Tennessee Warbler.
locations = get_nearest_species(api_key, 'tenwar', 42.48, -76.45)
```

Depending on what time of year you try this, you might have a long way to go.

### Checklists

There are two functions for finding out what has been seen at a given location.
First you can get the list of checklists for a given country, region or location
using get_visits(). Each result returned has the unique identifier for the
checklist. You can then call get_checklist() to get the list of observations.

```python
import os

from ebird.api.requests import get_visits, get_checklist

api_key = os.environ["EBIRD_API_KEY"]

# Get visits made recently to locations in New York state:
visits = get_visits(api_key, 'US-NY')

# Get visits made recently to locations in New York state on Jan 1st 2010
recent_visits = get_visits(api_key, 'US-NY', '2010-01-01')

# Get the details of a checklist
checklist = get_checklist(api_key, 'S22536787')
```

### Hotspots

There are two functions for discovering hotspots. get_hotspots() list all
the locations in a given area. You can find all the hotspots visited recently
by given a value for the back argument. get_nearby_hotspots() is used to find
hotspots within a given radius. get_hotspot() can be used to get information
on the location of a given hotspot.

```python
import os

from ebird.api.requests import get_hotspots, get_nearby_hotspots, get_hotspot

api_key = os.environ["EBIRD_API_KEY"]

# List all the hotspots in New York state.
hotspots = get_hotspots(api_key, 'US-NY')

# List all the hotspots in New York state visited in the past week.
recent = get_hotspots(api_key, 'US-NY', back=7)

# List all the hotspots in within 50kn of Point Reyes
nearby = get_nearby_hotspots(api_key, 38.05, -122.94, dist=50)

# Get the details of Anne V Pickard Memorial Wildlife Overlook in New York state.
details = get_hotspot(api_key, 'L2313391')
```

### Regions

eBird divides the world into countries, subnational1 regions (states) or
subnational2 regions (counties). You can use get_regions() to get the
list of sub-regions for a given region. For the approximate area covered
by a region use get_region().

```python
import os

from ebird.api.requests import get_regions, get_adjacent_regions, get_region

api_key = os.environ["EBIRD_API_KEY"]

# Get the list of countries in the world.
countries = get_regions(api_key, 'country', 'world')

# Get the list of states in the US.
states = get_regions(api_key, 'subnational1', 'US')

# Get the list of counties in New York state.
counties = get_regions(api_key, 'subnational2', 'US-NY')

# Get the list of states which border New York state.
nearby = get_adjacent_regions(api_key, 'US-NY')

# Get the approximate area covered by New York state.
bounds = get_region(api_key, 'US-NY')
```

### Taxonomy

You can get details of all the species, subspecies, forms
etc. in the taxonomy used by eBird. It's the easiest way
of getting the codes for each species or subspecies,
e.g. horlar (Horned Lark), cangoo (Canada Goose), etc.,
that are used in the other API calls.

```python
import os

from ebird.api.requests import get_taxonomy, get_taxonomy_forms, get_taxonomy_versions

api_key = os.environ["EBIRD_API_KEY"]

# Get all the species in the eBird taxonomy.
taxonomy = get_taxonomy(api_key)

# Get all the species in the eBird taxonomy with common names in Spanish
names = get_taxonomy(api_key, locale='es')

# Get all the taxonomy for Horned Lark
species = get_taxonomy(api_key, species='horlar')

# Get the codes for all the subspecies and froms recognised for Barn Swallow.
forms = get_taxonomy_forms(api_key, 'barswa')

# Get information on all the taxonomy revisions, i.e. versions.
# Usually only the latest is important.
versions = get_taxonomy_versions(api_key)
```

### Statistics

You can also get some statistics from the eBird data. The most interesting
is probably get_top_100() which returns the list of observers who have seen
the most species or submitted the largest number of checklists. The list is
just for a specific day so it is really only useful for "Big Days" when
lots of people are out trying to get the greatest number of species.

```python
import os

from datetime import date
from ebird.api.requests import get_top_100, get_totals

api_key = os.environ["EBIRD_API_KEY"]

# Get the winner of the Global Big Day in New York, on 5th May 2018
winners = get_top_100(api_key, 'US-NY', '2018-05-05')

# Get the number of contributors, checklist submitted and species seen today
totals = get_totals(api_key, 'US-NY', date.today())
```

### Client

There is a simple Client class which wraps the various functions from the API.
You can set the API key and locale when creating a Client instance so you don't
have to keep passing them as arguments.

```python
import os

from ebird.api.requests import Client

api_key = os.environ["EBIRD_API_KEY"]
locale = 'es'

client = Client(api_key, locale)

client.get_observations('MX-OAX')

```

The client supports all the API functions.

## Formats

Most of the eBird API calls return JSON. Some of the calls such as getting
the hotspots for a region or getting the taxonomy also support CSV. Since
converting JSON to CSV is simple this library is opinionated in that it
only returns JSON.

## Compatibility

ebird-api works with currently supported versions of Python, 3.10+. However,
it is known to work with earlier versions, at least 3.5 - 3.8, without any
problems.

## Troubleshooting

Just occasionally (rarely in fact), the connection to eBird will freeze. The
client will raise an error but if you use the API functions directly then your
program will sit there forever. To fix this set a default timeout all connections
using:

```python
import socket

socket.setdefaulttimeout(30)
```

Thirty seconds is a reasonable figure, however you might change it if your
internet connection is slow or the eBird servers are busy.

## Links

Documentation for the eBird API: https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest#intro
though it could do with a little love and attention.

Available translations for species names: http://help.ebird.org/customer/portal/articles/1596582

Information on the taxonomy used by eBird: http://help.ebird.org/customer/portal/articles/1006825-the-ebird-taxonomy

## License

eBird API is available under the terms of the [MIT](https://opensource.org/licenses/MIT) licence.
