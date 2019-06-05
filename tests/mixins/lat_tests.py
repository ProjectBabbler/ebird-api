from tests.mixins import BaseMixin


class LatTestsMixin(BaseMixin):

    def test_lat_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(lat='45.0'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['lat'], '45.00')  # noqa

    def test_invalid_lat_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lat='90.1'))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lat='-90.1'))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lat='x'))  # noqa
