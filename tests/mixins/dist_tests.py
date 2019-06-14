from ebird.api.constants import DEFAULT_DISTANCE
from tests.mixins import BaseMixin


class DistTestsMixin(BaseMixin):

    def test_dist_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(dist=50))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['dist'], 50)  # noqa

    def test_default_dist_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(dist=DEFAULT_DISTANCE))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('dist' not in actual)  # noqa

    def test_invalid_dist_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(dist=51))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(dist='x'))  # noqa
