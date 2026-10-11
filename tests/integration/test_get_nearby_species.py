from ebird.api.requests import get_nearby_species


def test_api_call(api_token, species_code, coordinates):
    observations = get_nearby_species(
        api_token, species_code, coordinates[0], coordinates[1]
    )
    for observation in observations:
        assert observation["speciesCode"] == species_code
