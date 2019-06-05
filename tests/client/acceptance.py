import datetime
import json

from urllib.error import HTTPError

from ebird.api import Client


def save_json(filename, data):
    with open(filename + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def check_client():

    area = 'PT-11'
    region = 'PT-11'
    rtype = 'subnational2'
    species = 'barswa'
    date = datetime.date.today()
    lat = '38.05'
    lng = '-122.94'
    loc_id = 'L2313391'
    sub_id = 'S56966468'

    api_key = 's46vrls4eibf'
    locale = 'en'

    try:
        client = Client(api_key, locale)

        save_json('get_observations', client.get_observations(area))

        save_json('get_notable_observations', client.get_notable_observations(area))

        save_json('get_species_observations', client.get_species_observations(species, area))

        save_json('get_historic_observations', client.get_historic_observations(area, date))

        save_json('get_nearby_observations', client.get_nearby_observations(lat, lng, dist=25))

        save_json('get_nearby_notable', client.get_nearby_notable(lat, lng, dist=25))

        save_json('get_nearby_species', client.get_nearby_species(species, lat, lng, dist=25))

        save_json('get_nearest_species', client.get_nearest_species(species, lat, lng, dist=25))

        save_json('get_hotspots', client.get_hotspots(area, back=14))

        save_json('get_nearby_hotspots', client.get_nearby_hotspots(lat, lng, dist=25))

        save_json('get_hotspot', client.get_hotspot(loc_id))

        save_json('get_regions', client.get_regions(rtype, region))

        save_json('get_adjacent_regions', client.get_adjacent_regions(region))

        save_json('get_region', client.get_region(region))

        save_json('get_visits', client.get_visits(area, date))

        save_json('get_checklist', client.get_checklist(sub_id))

        save_json('get_top_100', client.get_top_100(region, date))

        save_json('get_totals', client.get_totals(area, date))

        save_json('get_taxonomy', client.get_taxonomy())

        save_json('get_taxonomy_forms', client.get_taxonomy_forms(species))

        save_json('get_taxonomy_groups', client.get_taxonomy_groups())

        save_json('get_taxonomy_versions', client.get_taxonomy_versions())

    except HTTPError as err:
        print(err, err.filename)


if __name__ == '__main__':
    check_client()
