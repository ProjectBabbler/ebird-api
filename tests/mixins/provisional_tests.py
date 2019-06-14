from ebird.api.constants import DEFAULT_PROVISIONAL
from tests.mixins import BaseMixin


class ProvisionalTestsMixin(BaseMixin):

    def test_include_provisional_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(provisional=True))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['includeProvisional'], 'true')  # noqa

    def test_default_include_provisional_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(provisional=DEFAULT_PROVISIONAL == 'true'))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('includeProvisional' not in actual)  # noqa
