from tests.mixins import BaseMixin


class BackTestsMixin(BaseMixin):

    def test_back_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(back=10))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['back'], 10)  # noqa

    def test_default_back_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params())
        actual = mocked_function.call_args[0][1]
        self.assertTrue('back' not in actual)  # noqa

    def test_invalid_back_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(back=31))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(back='x'))  # noqa
