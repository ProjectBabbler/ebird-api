from tests.mixins import BaseMixin


class LngTestsMixin(BaseMixin):

    def test_lng_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(lng='90.0'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['lng'], '90.00')  # noqa

    def test_invalid_lng_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lng='180.1'))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lng='-180.1'))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(lng='x'))  # noqa
