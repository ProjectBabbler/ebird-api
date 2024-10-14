from tests.unit.mixins.base import BaseMixin


class LocationTestsMixin(BaseMixin):
    def test_location_is_comma_separated_string(self):
        query = self.api_call(locations="L001,L002")[1]
        self.assertTrue(query["r"], "L001,L002")

    def test_location_string_whitespace_is_removed(self):
        query = self.api_call(locations=" L001 , L002 ")[1]
        self.assertTrue(query["r"], "L001,L002")

    def test_location_is_list(self):
        query = self.api_call(locations=["L001", "L002"])[1]
        self.assertTrue(query["r"], "L001,US_ID")

    def test_location_list_whitespace_is_removed(self):
        query = self.api_call(locations=[" L001 ", " L002 "])[1]
        self.assertTrue(query["r"], "L001,L002")

    def test_invalid_location_raises_error(self):
        self.api_raises(ValueError, locations="L")

    def test_blank_location_raises_error(self):
        self.api_raises(ValueError, locations="")

    def test_blank_location_in_string_raises_error(self):
        self.api_raises(ValueError, locations="L001,")

    def test_blank_location_in_list_raises_error(self):
        self.api_raises(ValueError, locations=["L001", ""])

    def test_more_than_10_in_string_raises_error(self):
        self.api_raises(ValueError, locations=",".join(["L001"] * 11))

    def test_more_than_10_in_list_raises_error(self):
        self.api_raises(ValueError, locations=["L001"] * 11)
