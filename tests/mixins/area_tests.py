from unittest import skip

from tests.mixins import BaseMixin


class AreaTestsMixin(BaseMixin):

    def test_location_is_string(self):
        url = self.api_call(area='US-NV')[0]
        self.assertTrue('/US-NV/' in url)

    def test_location_is_comma_separated_string(self):
        query = self.api_call(area='US-NV,US-ID')[1]
        self.assertTrue(query['r'], 'US-NV,US-ID')

    def test_location_is_included_in_url(self):
        url = self.api_call(area='US-NV,US-ID')[0]
        self.assertTrue('/US-NV/' in url)

    def test_location_string_whitespace_is_removed(self):
        query = self.api_call(area=' US-NV , US-ID ')[1]
        self.assertTrue(query['r'], 'US-NV,US-ID')

    def test_location_is_list(self):
        query = self.api_call(area=['US-NV', 'US-ID'])[1]
        self.assertTrue(query['r'], 'US-NV,US_ID')

    def test_location_list_whitespace_is_removed(self):
        query = self.api_call(area=[' US-NV ', ' US-ID '])[1]
        self.assertTrue(query['r'], 'US-NV,US_ID')

    def test_first_location_is_included_in_url(self):
        url = self.api_call(area=['US-NV', 'US-ID'])[0]
        self.assertTrue('/US-NV/' in url)

    def test_invalid_location_raises_error(self):
        self.api_raises(ValueError, area='U')

    def test_blank_location_raises_error(self):
        self.api_raises(ValueError, area='')

    def test_blank_location_in_string_raises_error(self):
        self.api_raises(ValueError, area='US-NV,')

    def test_blank_location_in_list_raises_error(self):
        self.api_raises(ValueError, area=['US', ''])

    @skip('Disabled as API currently allows more than 10 locations')
    def test_more_than_10_in_string_raises_error(self):
        self.api_raises(ValueError, area=','.join(['US'] * 11))

    @skip('Disabled as API currently allows more than 10 locations')
    def test_more_than_10_in_list_raises_error(self):
        self.api_raises(ValueError, area=['US'] * 11)
