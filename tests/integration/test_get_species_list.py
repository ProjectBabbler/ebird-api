from ebird.api.requests import get_species_list


def test_api_call(api_token, subnational1_code):
    species = get_species_list(api_token, subnational1_code)
    assert len(species)
