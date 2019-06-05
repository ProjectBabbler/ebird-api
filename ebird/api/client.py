from ebird.api import observations, checklists, regions, hotspots, \
    taxonomy, statistics


class Client:
    """Client class to simplify interacting with the API calls.

    The arguments used to initialize the client are generally API parameters
    which stay relatively fixed for a given application, e.g. including records
    which have not been reviewed (provisional = True) or to include records from
    private and hotspot locations (hotspots = False).

    """

    def __init__(self, api_key, locale):
        self.api_key = api_key

        self.locale = locale
        self.sppLocale = locale
        self.groupNameLocale = locale

        self.max_observations = None
        self.max_visits = 200
        self.max_observers = 100

        self.back = 14
        self.category = None
        self.detail = 'full'
        self.dist = 25
        self.hotspot = False
        self.provisional = True
        self.sort = 'date'

    def get_observations(self, area):
        return observations.get_observations(
            self.api_key, area,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot, detail=self.detail,
            category=self.category)

    def get_notable_observations(self, area):
        return observations.get_notable_observations(
            self.api_key, area,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            hotspot=self.hotspot, detail=self.detail)

    def get_species_observations(self, species, area):
        return observations.get_species_observations(
            self.api_key, species, area,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot, detail=self.detail,
            category=self.category)

    def get_historic_observations(self, area, date):
        return observations.get_historic_observations(
            self.api_key, area, date,
            max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot, detail=self.detail,
            category=self.category)

    def get_nearby_observations(self, lat, lng, dist=25):
        return observations.get_nearby_observations(
            self.api_key, lat, lng, dist=dist,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot,
            category=self.category)

    def get_nearby_notable(self, lat, lng, dist=25):
        return observations.get_nearby_notable(
            self.api_key, lat, lng, dist=dist,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            hotspot=self.hotspot, detail=self.detail)

    def get_nearby_species(self, species, lat, lng, dist=25):
        return observations.get_nearby_species(
            self.api_key, species, lat, lng, dist=dist,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot,
            category=self.category)

    def get_nearest_species(self, species, lat, lng, dist=25):
        return observations.get_nearest_species(
            self.api_key, species, lat, lng, dist=dist,
            back=self.back, max_results=self.max_observations, locale=self.locale,
            provisional=self.provisional, hotspot=self.hotspot)

    def get_hotspots(self, region, back=14):
        return hotspots.get_hotspots(self.api_key, region, back)

    def get_nearby_hotspots(self, lat, lng, dist=25):
        return hotspots.get_nearby_hotspots(self.api_key, lat, lng, dist, back=self.back)

    def get_hotspot(self, loc_id):
        return hotspots.get_hotspot(self.api_key, loc_id)

    def get_regions(self, rtype, region):
        return regions.get_regions(self.api_key, rtype, region)

    def get_adjacent_regions(self, region):
        return regions.get_adjacent_regions(self.api_key, region)

    def get_region(self, region):
        return regions.get_region(self.api_key, region)

    def get_visits(self, area, date=None):
        return checklists.get_visits(self.api_key, area, date, max_results=self.max_visits)

    def get_checklist(self, subid):
        return checklists.get_checklist(self.api_key, subid)

    def get_top_100(self, region, date):
        return statistics.get_top_100(self.api_key, region, date, max_results=self.max_observers)

    def get_totals(self, area, date):
        return statistics.get_totals(self.api_key, area, date)

    def get_taxonomy(self):
        return taxonomy.get_taxonomy(self.api_key, self.category, locale=self.locale)

    def get_taxonomy_forms(self, code):
        return taxonomy.get_taxonomy_forms(self.api_key, code)

    def get_taxonomy_groups(self):
        return taxonomy.get_taxonomy_groups(self.api_key, locale=self.locale)

    def get_taxonomy_versions(self):
        return taxonomy.get_taxonomy_versions(self.api_key)
