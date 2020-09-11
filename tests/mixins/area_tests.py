from tests.mixins.base import BaseMixin


class AreaTestsMixin(BaseMixin):
    def test_area_can_be_country(self):
        url = self.api_call(area="US")[0]
        self.assertTrue("/US/" in url)

    def test_area_can_be_subnational1(self):
        url = self.api_call(area="US-NY")[0]
        self.assertTrue("/US-NY/" in url)

    def test_area_can_be_subnational2(self):
        url = self.api_call(area="US-NY-001")[0]
        self.assertTrue("/US-NY-001/" in url)

    def test_area_can_be_location(self):
        url = self.api_call(area="L123456")[0]
        self.assertTrue("/L123456/" in url)

    def test_area_can_be_comma_separated_string(self):
        query = self.api_call(area="US-NV,US-ID")[1]
        self.assertTrue(query["r"], "US-NV,US-ID")

    def test_area_can_be_list(self):
        query = self.api_call(area=["US-NV", "US-ID"])[1]
        self.assertTrue(query["r"], "US-NV,US_ID")

    def test_string_has_whitespace_removed(self):
        query = self.api_call(area=" US-NV , US-ID ")[1]
        self.assertTrue(query["r"], "US-NV,US-ID")

    def test_list_has_whitespace_removed(self):
        query = self.api_call(area=[" US-NV ", " US-ID "])[1]
        self.assertTrue(query["r"], "US-NV,US_ID")

    def test_first_area_is_included_in_url(self):
        url = self.api_call(area=["US-NV", "US-ID"])[0]
        self.assertTrue("/US-NV/" in url)

    def test_invalid_area_raises_error(self):
        self.api_raises(ValueError, area="U")

    def test_blank_area_raises_error(self):
        self.api_raises(ValueError, area="")

    def test_blank_area_in_string_raises_error(self):
        self.api_raises(ValueError, area="US-NV,")

    def test_blank_area_in_list_raises_error(self):
        self.api_raises(ValueError, area=["US", ""])

    def test_more_than_10_area_in_string_raises_error(self):
        self.api_raises(ValueError, area=",".join(["US"] * 11))

    def test_more_than_10_area_in_list_raises_error(self):
        self.api_raises(ValueError, area=["US"] * 11)

    def test_mixing_area_types_in_string_raises_error(self):
        self.api_raises(ValueError, area="US,Us-NV")

    def test_mixing_area_types_in_list_raises_error(self):
        self.api_raises(ValueError, area=["US", "Us-NV"])
