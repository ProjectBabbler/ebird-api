from ebird.api.requests import get_regions


def test_api_call(api_token, subnational1_code):
    regions = get_regions(api_token, "subnational2", subnational1_code)
    for region in regions:
        assert region["code"].startswith(subnational1_code)
