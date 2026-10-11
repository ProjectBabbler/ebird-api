import os

import pytest

from ebird.api.requests import get_hotspots


@pytest.fixture(scope="session")
def api_token():
    return os.environ["EBIRD_API_KEY"]


@pytest.fixture(scope="session")
def subnational1_code():
    return "US-MA"


@pytest.fixture(scope="session")
def coordinates(api_token, subnational1_code):
    hotspots = get_hotspots(api_token, subnational1_code)
    return hotspots[0]["lat"], hotspots[0]["lng"]


@pytest.fixture(scope="session")
def species_code():
    return "mallar3"  # mallard
