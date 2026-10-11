from unittest import TestCase

from ebird.api.requests.checklists import CHECKLIST_URL, get_checklist
from tests.unit.mixins import HeaderTestsMixin


class GetChecklistTests(TestCase, HeaderTestsMixin):
    """Tests for the get_checklist() API call."""

    def get_callable(self):
        return get_checklist

    def get_params(self, **kwargs):
        params = {
            "token": "12345",
            "sub_id": "S12345678",
        }
        params.update(kwargs)
        return params

    def test_request_url(self):
        url = self.api_call()[0]
        self.assertEqual(CHECKLIST_URL % "S12345678", url)
