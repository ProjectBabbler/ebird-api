from tests.mixins import BaseMixin


class LatTestsMixin(BaseMixin):

    def test_lat_is_sent(self):
        query = self.api_call(lat='45.0')[1]
        self.assertEqual(query['lat'], '45.00')

    def test_invalid_lat_raises_error(self):
        self.api_raises(ValueError, lat='90.1')
        self.api_raises(ValueError, lat='-90.1')
        self.api_raises(ValueError, lat='x')
