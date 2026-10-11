from ebird.api.requests import get_visits


def test_api_call(api_token, subnational1_code):
    default_number_of_visits = 10
    visits = get_visits(api_token, subnational1_code)
    expected = [subnational1_code] * default_number_of_visits
    actual = [visit["loc"]["subnational1Code"] for visit in visits]
    assert actual == expected
