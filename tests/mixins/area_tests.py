from tests.mixins import BaseMixin


class AreaTestsMixin(BaseMixin):

    def test_location_is_string(self, mocked_function):
        self.get_fixture()(**self.get_params(area='US-NV'))
        actual = mocked_function.call_args[0][0]
        self.assertTrue('/US-NV/' in actual)  # noqa

    def test_location_is_comma_separated_string(self, mocked_function):
        self.get_fixture()(**self.get_params(area='US-NV,US-ID'))
        actual = mocked_function.call_args[0][1]
        self.assertTrue(actual['r'], 'US-NV,US-ID')  # noqa

    def test_location_is_included_in_url(self, mocked_function):
        self.get_fixture()(**self.get_params(area='US-NV,US-ID'))
        actual = mocked_function.call_args[0][0]
        self.assertTrue('/US-NV/' in actual)  # noqa

    def test_location_string_whitespace_is_removed(self, mocked_function):
        self.get_fixture()(**self.get_params(area=' US-NV , US-ID '))
        actual = mocked_function.call_args[0][1]
        self.assertTrue(actual['r'], 'US-NV,US-ID')  # noqa

    def test_location_is_list(self, mocked_function):
        self.get_fixture()(**self.get_params(area=['US-NV', 'US-ID']))
        actual = mocked_function.call_args[0][1]
        self.assertTrue(actual['r'], 'US-NV,US_ID')  # noqa

    def test_location_list_whitespace_is_removed(self, mocked_function):
        self.get_fixture()(**self.get_params(area=[' US-NV ', ' US-ID ']))
        actual = mocked_function.call_args[0][1]
        self.assertTrue(actual['r'], 'US-NV,US_ID')  # noqa

    def test_first_location_is_included_in_url(self, mocked_function):
        self.get_fixture()(**self.get_params(area=['US-NV', 'US-ID']))
        actual = mocked_function.call_args[0][0]
        self.assertTrue('/US-NV/' in actual)  # noqa

    def test_invalid_location_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area='U'))  # noqa

    def test_blank_location_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area=''))  # noqa

    def test_blank_location_in_string_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area='US-NV,'))  # noqa

    def test_blank_location_in_list_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area=['US', '']))  # noqa

    def test_more_than_10_in_string_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area=','.join(['US']*11)))  # noqa

    def test_more_than_10_in_list_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(area=['US']*11))  # noqa
