from ebird.api.base import PARAMETER_DEFAULTS
from tests.mixins import BaseMixin


class SortTestsMixin(BaseMixin):

    def test_sort_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(sort='species'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['sort'], 'species')  # noqa

    def test_default_sort_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(sort=PARAMETER_DEFAULTS['sort']))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('sort' not in actual)  # noqa

    def test_invalid_sort_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(sort='none'))  # noqa
