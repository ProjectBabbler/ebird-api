# pylint: disable=R0902,R0904

"""Classes for simplifying calls to the eBird API."""

import socket

from ebird.api.requests import (
    checklists,
    constants,
    hotspots,
    observations,
    regions,
    statistics,
    taxonomy,
)
from ebird.api.requests.validation import clean_locale


class Client:
    """Client class to simplify interacting with the API calls.

    The arguments used to initialize the client are generally API parameters
    which stay relatively fixed for a given application, e.g. including records
    which have not been reviewed (provisional = True) or to include records
    from private and hotspot locations (hotspots = False).

    All methods raise ValueError if any of the arguments or default values
    cannot be validated; URLError if there is an error with the connection
    to the eBird site or HTTPError if the eBird API returns an error.

    """

    def __init__(self, api_key, locale):
        self.api_key = api_key
        self.locale = clean_locale(locale)
        self.max_observations = None
        self.max_visits = constants.API_MAX_RESULTS
        self.max_observers = constants.DEFAULT_MAX_OBSERVERS
        self.back = constants.DEFAULT_BACK
        self.category = None
        self.detail = "full"
        self.dist = constants.DEFAULT_DISTANCE
        self.hotspot = False
        self.provisional = True
        self.sort = "date"
        socket.setdefaulttimeout(constants.DEFAULT_TIMEOUT)

    def get_observations(self, area):
        """Get recent observations (up to 30 days ago) for a region or location.

        :param area: a country, subnational1, subnational2 or location code
        or a list of up to 10 codes. All codes must be same type.

        :return: the list of observations in simple format.

        """
        return observations.get_observations(
            self.api_key,
            area,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
            detail=self.detail,
            category=self.category,
        )

    def get_notable_observations(self, area):
        """Get recent observations of a rare species for a region or location

        :param area: a country, subnational1, subnational2 or location code
        or a list of up to 10 codes. All codes must be same type.

        :return: the list of observations.

        """
        return observations.get_notable_observations(
            self.api_key,
            area,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            hotspot=self.hotspot,
            detail=self.detail,
        )

    def get_species_observations(self, species, area):
        """Get recent observations for a given species in a region.

        :param species: the scientific name of the species.

        :param area: a country, subnational1, subnational2 or location code
        or a list of up to 10 codes. All codes must be same type.

        :return: the list of observations in simple format.

        """
        return observations.get_species_observations(
            self.api_key,
            species,
            area,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
            detail=self.detail,
            category=self.category,
        )

    def get_historic_observations(self, area, date):
        """Get recent observations for a region.

        :param area: a country, subnational1, subnational2 or location code
        or a list of up to 10 codes. All codes must be same type.

        :param date: the date, since Jan 1st 1800.

        :return: the list of observations in simple format.

        """
        return observations.get_historic_observations(
            self.api_key,
            area,
            date,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
            detail=self.detail,
            category=self.category,
        )

    def get_nearby_observations(self, lat, lng, dist=25):
        """Get nearby recent observations of each species.

        :param lat: the latitude, which will be rounded to 2 decimal places.

        :param lng: the longitude, which will be rounded to 2 decimal places.

        :param dist: include all sites within this distance, from 0 to 50km
        with a default of 25km.

        :return: the list of observations in simple format.

        """
        return observations.get_nearby_observations(
            self.api_key,
            lat,
            lng,
            dist=dist,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
            category=self.category,
        )

    def get_nearby_notable(self, lat, lng, dist=25):
        """Get the nearby, recent observations of rare species.

        :param lat: the latitude, which will be rounded to 2 decimal places.

        :param lng: the longitude, which will be rounded to 2 decimal places.

        :param dist: include all sites within this distance, from 0 to 50km
        with a default of 25km.

        :return: the list of observations.

        """
        return observations.get_nearby_notable(
            self.api_key,
            lat,
            lng,
            dist=dist,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            hotspot=self.hotspot,
            detail=self.detail,
        )

    def get_nearby_species(self, species, lat, lng, dist=25):
        """Get most recent observation of a species nearby.

        :param species: the scientific name of the species.

        :param lat: the latitude, which will be rounded to 2 decimal places.

        :param lng: the longitude, which will be rounded to 2 decimal places.

        :param dist: include all sites within this distance, from 0 to 50km
        with a default of 25km.

        :return: the list of observations in 'simple' form. See the eBird API
        documentation for a description of the fields.

        """
        return observations.get_nearby_species(
            self.api_key,
            species,
            lat,
            lng,
            dist=dist,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
            category=self.category,
        )

    def get_nearest_species(self, species, lat, lng, dist=25):
        """Get most recent observation of a species nearby.

        :param species: the scientific name of the species.

        :param lat: the latitude, which will be rounded to 2 decimal places.

        :param lng: the longitude, which will be rounded to 2 decimal places.

        :param dist: include all sites within this distance, from 0 to 50km
        with a default of 25km.

        :return: the list of observations in 'simple' form.

        """
        return observations.get_nearest_species(
            self.api_key,
            species,
            lat,
            lng,
            dist=dist,
            back=self.back,
            max_results=self.max_observations,
            locale=self.locale,
            provisional=self.provisional,
            hotspot=self.hotspot,
        )

    def get_hotspots(self, region, back=14):
        """List all hotspots within a region.

        :param region: the code for a country, subnational1 or subnational2 region.

        :param back: the past number of days to check, default is 14.

        :return: the list of hotspots.

        """
        return hotspots.get_hotspots(self.api_key, region, back)

    def get_nearby_hotspots(self, lat, lng, dist=25):
        """Get the list of nearby hotspots.

        :param lat: the latitude, which will be rounded to 2 decimal places.

        :param lng: the longitude, which will be rounded to 2 decimal places.

        :param dist: include all sites within this distance, from 0 to 50km
        with a default of 25km.

        :return: the list of hotspots nearest to the given set of coordinates.

        """
        return hotspots.get_nearby_hotspots(
            self.api_key, lat, lng, dist, back=self.back
        )

    def get_hotspot(self, loc_id):
        """Get the geographical details of a hotspot.

        :param loc_id: the location code for a hotspot, eg. L374326.

        :return: the latitude, longitude, name, region, etc. for the hotspot.

        """
        return hotspots.get_hotspot(self.api_key, loc_id)

    def get_regions(self, rtype, region):
        """Get the list of sub-regions or a given region.

        :param rtype: the region type, either 'country', 'subnational1'
        or 'subnational2'.

        :param region: the name of the region, either 'world', a country
        or a subnational1 code.

        :return: the list of sub-regions within the given region.

        """
        return regions.get_regions(self.api_key, rtype, region)

    def get_adjacent_regions(self, region):
        """Get the regions adjacent to a given region.

        :param region: the name of the region, either a country, a subnational1
        or a subnational2 code.

        :return: the list of regions bordering the specified region.

        """
        return regions.get_adjacent_regions(self.api_key, region)

    def get_region(self, region):
        """Get the geographical details of a country, region or sub-region.

        :param region: the code for the region, eg. US-NV.

        :return: the latitude, longitude, name, region, etc. for the area.

        """
        return regions.get_region(self.api_key, region)

    def get_visits(self, area, date=None):
        """
        Get the list of checklists for an area. The most recent checklists are
        returned if a specific date is not given.

        :param area: the code for a country, subnational1 region, subnational2
        region or location.

        :param date: the date, since Jan 1st 1800.

        :return: the info for all the checklists submitted.

        """
        return checklists.get_visits(
            self.api_key, area, date, max_results=self.max_visits
        )

    def get_checklist(self, sub_id):
        """
        Get the contents of a checklist.

        :param sub_id: the unique identifier for the checklist, e.g. S22893621.

        :return: the details of the checklist, including the list of observations

        """
        return checklists.get_checklist(self.api_key, sub_id)

    def get_top_100(self, region, date, rank="spp"):
        """
        Get the observers who have seen the most species or submitted the
        greatest number of checklists on a given date.

        :param region: the code for the region, eg. US-NV.

        :param date: the date, since Jan 1st 1800.

        :param rank: rank the observers by species seen (spp) or number of
        checklists submitted (cl).

        :return: the list of observers.

        """
        return statistics.get_top_100(
            self.api_key, region, date, rank=rank, max_results=self.max_observers
        )

    def get_totals(self, area, date):
        """
        Get the number of contributors, checklists submitted and species
        seen on a given date.

        :param area: the code for a country subnational1 , subnational2
        region or location

        :param date: the date, since Jan 1st 1800.

        :return: the totals for the given date

        """
        return statistics.get_totals(self.api_key, area, date)

    def get_taxonomy(self):
        """Get the full or specific subset of the taxonomy used by eBird.

        :return: the complete list of species used by eBird.

        """
        return taxonomy.get_taxonomy(self.api_key, self.category, locale=self.locale)

    def get_taxonomy_forms(self, code):
        """Get all the sub-specific forms of a given species.

        :return: the list of codes of each sub-species.

        """
        return taxonomy.get_taxonomy_forms(self.api_key, code)

    def get_taxonomy_groups(self):
        """Get the names of the groups of species used in the taxonomy.

        :return: the list of species groups.

        """
        return taxonomy.get_taxonomy_groups(self.api_key, locale=self.locale)

    def get_taxonomy_versions(self):
        """Get all versions of the taxonomy, indicating which is the latest.

        :return: a list of all the taxonomy versions used by eBird.

        """
        return taxonomy.get_taxonomy_versions(self.api_key)
