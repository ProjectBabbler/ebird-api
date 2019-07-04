from tests.mixins import BaseMixin


class HeaderTestsMixin(BaseMixin):

    def test_api_key_in_header(self):
        headers = self.api_call(token='abc123')[2]
        self.assertEqual(headers['X-eBirdApiToken'], 'abc123')
