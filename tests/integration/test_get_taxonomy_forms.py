from ebird.api.requests import get_taxonomy_forms


def test_api_call(api_token):
    species_code = "horlar"
    forms = get_taxonomy_forms(api_token, species_code)
    for form in forms:
        assert form.startswith(species_code)
