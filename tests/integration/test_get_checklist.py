from ebird.api.requests import get_checklist, get_visits


def test_api_call(api_token, subnational1_code):
    visits = get_visits(api_token, subnational1_code)
    for visit in visits:
        checklist = get_checklist(api_token, visit["subId"])
        assert checklist["subId"] == visit["subId"]
