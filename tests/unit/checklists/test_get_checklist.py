# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from ebird.api.checklists import CHECKLIST_URL, get_checklist

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.checklists.get_content', side_effect=get_content)
class GetChecklistTests(mixins.HeaderTestsMixin, TestCase):
    """Tests for the get_checklist() API call."""

    def get_fixture(self):
        return get_checklist

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
            'sub_id': 'S12345678',
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(CHECKLIST_URL % 'S12345678', actual)
