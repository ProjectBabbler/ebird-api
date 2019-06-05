from ebird.api.base import PARAMETER_DEFAULTS
from tests.mixins import BaseMixin


class CategoryTestsMixin(BaseMixin):

    def test_category_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(category='species'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['cat'], 'species')  # noqa

    def test_default_category_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(category=PARAMETER_DEFAULTS['cat']))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('cat' not in actual)  # noqa

    def test_invalid_category_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(category='none'))  # noqa
