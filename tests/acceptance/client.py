import datetime
import os

from ebird.api import Client
from ebird.api.utils import save_json

area = 'PT-11'
region = 'PT-11'
rtype = 'subnational2'
species = 'barswa'
date = datetime.date.today()
lat = '38.05'
lng = '-122.94'
locale = 'en'
loc_id = 'L2313391'
sub_id = 'S56966468'
result_dir = 'tests/results'


def save_results(filename, results):
    path = os.path.join(result_dir, filename)
    save_json(path, results)


client = Client(os.environ['EBIRD_API_KEY'], locale)

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

save_results('get_observations', client.get_observations(area))
save_results('get_notable_observations', client.get_notable_observations(area))
save_results('get_species_observations', client.get_species_observations(species, area))
save_results('get_historic_observations', client.get_historic_observations(area, date))
save_results('get_nearby_observations', client.get_nearby_observations(lat, lng, dist=25))
save_results('get_nearby_notable', client.get_nearby_notable(lat, lng, dist=25))
save_results('get_nearby_species', client.get_nearby_species(species, lat, lng, dist=25))
save_results('get_nearest_species', client.get_nearest_species(species, lat, lng, dist=25))
save_results('get_hotspots', client.get_hotspots(area, back=14))
save_results('get_nearby_hotspots', client.get_nearby_hotspots(lat, lng, dist=25))
save_results('get_hotspot', client.get_hotspot(loc_id))
save_results('get_regions', client.get_regions(rtype, region))
save_results('get_adjacent_regions', client.get_adjacent_regions(region))
save_results('get_region', client.get_region(region))
save_results('get_visits', client.get_visits(area, date))
save_results('get_checklist', client.get_checklist(sub_id))
save_results('get_top_100', client.get_top_100(region, date))
save_results('get_totals', client.get_totals(area, date))
save_results('get_taxonomy', client.get_taxonomy())
save_results('get_taxonomy_forms', client.get_taxonomy_forms(species))
save_results('get_taxonomy_groups', client.get_taxonomy_groups())
save_results('get_taxonomy_versions', client.get_taxonomy_versions())
