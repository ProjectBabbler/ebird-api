from ebird.api.requests import get_taxonomy_versions


def test_api_call(api_token):
    versions = get_taxonomy_versions(api_token)
    assert versions[0]["latest"] is True
