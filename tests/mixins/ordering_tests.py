from ebird.api.base import PARAMETER_DEFAULTS
from tests.mixins import BaseMixin


class OrderingTestsMixin(BaseMixin):

    def test_ordering_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(ordering='merlin'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['speciesGrouping'], 'species')  # noqa

    def test_default_ordering_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(ordering=PARAMETER_DEFAULTS['ordering']))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('speciesGrouping' not in actual)  # noqa

    def test_invalid_ordering_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(ordering='none'))  # noqa
