# flake8: noqa

"""A set of wrapper functions for accessing the eBird API."""

__version__ = "3.2.2"

from ebird.api.checklists import get_checklist, get_visits
from ebird.api.client import Client
from ebird.api.constants import LOCALES
from ebird.api.hotspots import get_hotspot, get_hotspots, get_nearby_hotspots
from ebird.api.observations import (
    get_historic_observations,
    get_nearby_notable,
    get_nearby_observations,
    get_nearby_species,
    get_nearest_species,
    get_notable_observations,
    get_observations,
    get_species_observations,
)
from ebird.api.regions import get_adjacent_regions, get_region, get_regions
from ebird.api.species import get_species_list
from ebird.api.statistics import get_top_100, get_totals
from ebird.api.taxonomy import (
    get_taxonomy,
    get_taxonomy_forms,
    get_taxonomy_groups,
    get_taxonomy_locales,
    get_taxonomy_versions,
)
