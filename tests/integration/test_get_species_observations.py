from ebird.api.requests import get_species_observations


def test_api_call(api_token, species_code, subnational1_code):
    observations = get_species_observations(api_token, species_code, subnational1_code)
    for observation in observations:
        assert observation["speciesCode"] == species_code
