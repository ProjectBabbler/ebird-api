from datetime import date
from unittest import TestCase

from ebird.api.requests.observations import (
    HISTORIC_OBSERVATIONS_URL,
    get_historic_observations,
)
from ebird.api.requests import constants

from tests.unit import mixins


class GetHistoricObservationsTests(
    TestCase,
    mixins.AreaTestsMixin,
    mixins.CategoryTestsMixin,
    mixins.DetailTestsMixin,
    mixins.HeaderTestsMixin,
    mixins.HotspotTestsMixin,
    mixins.MaxObservationsTestsMixin,
    mixins.ProvisionalTestsMixin,
    mixins.SpeciesLocaleTestsMixin,
):
    """Tests for the get_historic_observations() API call."""

    def get_max_results_default(self):
        return None

    def get_callable(self):
        return get_historic_observations

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "area": "US-NV",
            "date": date.today(),
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        params = self.get_params()
        url = self.api_call()[0]
        self.assertEqual(
            HISTORIC_OBSERVATIONS_URL
            % (params["area"], params["date"].strftime("%Y/%m/%d")),
            url,
        )

    def test_request_for_multiple_areas_url(self):
        params = self.get_params(area="US-NV,US-WY,US-AZ")
        url = self.api_call()[0]
        self.assertEqual(
            HISTORIC_OBSERVATIONS_URL % ("US-NV", params["date"].strftime("%Y/%m/%d")),
            url,
        )

    def test_request_for_multiple_areas_parameter(self):
        query = self.api_call(area="US-NV,US-WY,US-AZ")[1]
        self.assertEqual(query["r"], "US-NV,US-WY,US-AZ")

    def test_that_rank_is_sent(self):
        query = self.api_call(rank="create")[1]
        self.assertEqual(query["rank"], "create")

    def test_that_mrec_is_default(self):
        query = self.api_call()[1]
        self.assertEqual(query["rank"], "mrec")

    def test_that_rank_is_valid(self):
        with self.assertRaises(ValueError) as value_error:
            self.api_call(rank="none")

        self.assertEqual(
            str(value_error.exception),
            f"Value for 'rank', none, must be in the set {constants.HISTORIC_RANKING_TYPES}.",
        )
