from unittest import TestCase
from unittest.mock import patch

from ebird.api.taxonomy import TAXONOMY_VERSIONS_URL, get_taxonomy_versions

from tests import mixins


def get_content(url, params, headers):  # noqa
    return '[]'


@patch('ebird.api.taxonomy.get_content', side_effect=get_content)
class GetTaxonomyVersionsTests(mixins.HeaderTestsMixin, TestCase):
    """Tests for the get_taxonomy_versions() API call."""

    def get_fixture(self):
        return get_taxonomy_versions

    def get_params(self, **kwargs):
        params = {
            'token': self.get_token(),
        }
        params.update(kwargs)
        return params

    def test_request_url(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][0]
        self.assertEqual(TAXONOMY_VERSIONS_URL, actual)

    def test_query_params_are_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][1]
        self.assertDictEqual({}, actual)
