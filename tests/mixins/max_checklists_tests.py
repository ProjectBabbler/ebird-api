from ebird.api.constants import DEFAULT_MAX_CHECKLISTS
from tests.mixins import BaseMixin


class MaxChecklistsTestsMixin(BaseMixin):

    def test_max_results_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(max_results=1))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['maxResults'], 1)  # noqa

    def test_default_max_results_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(max_results=DEFAULT_MAX_CHECKLISTS))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('maxResults' not in actual)  # noqa

    def test_invalid_max_results_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(max_results=0))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(max_results=201))  # noqa
