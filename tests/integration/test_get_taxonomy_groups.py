from ebird.api.requests import get_taxonomy_groups


def test_api_call(api_token):
    groups = get_taxonomy_groups(api_token, "ebird")
    assert groups[0]["groupName"] == "Ostriches"
