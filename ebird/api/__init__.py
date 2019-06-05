# -*- coding: utf-8 -*-

"""A set of wrapper functions for accessing the eBird API."""

__version__ = '3.0.0'

from ebird.api.observations import (
    get_observations,
    get_notable_observations,
    get_species_observations,
    get_nearby_observations,
    get_nearby_notable,
    get_nearby_species,
    get_nearest_species,
    get_historic_observations,
)

from ebird.api.checklists import (
    get_visits,
    get_checklist,
)

from ebird.api.hotspots import (
    get_hotspots,
    get_nearby_hotspots,
    get_hotspot,
)

from ebird.api.regions import (
    get_regions,
    get_region,
    get_adjacent_regions,
)

from ebird.api.statistics import (
    get_top_100,
    get_totals,
)

from ebird.api.taxonomy import (
    get_taxonomy,
    get_taxonomy_forms,
    get_taxonomy_groups,
    get_taxonomy_versions
)

from ebird.api.client import Client
