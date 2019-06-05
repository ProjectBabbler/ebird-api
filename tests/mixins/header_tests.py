from tests.mixins import BaseMixin


class HeaderTestsMixin(BaseMixin):

    def test_api_key_in_header(self, mocked_function):
        self.get_fixture()(**self.get_params(token='abc123'))
        actual = mocked_function.call_args[0][2]
        self.assertEqual(actual['X-eBirdApiToken'], 'abc123')  # noqa
