from ebird.api.constants import DEFAULT_DETAIL
from tests.mixins import BaseMixin


class DetailTestsMixin(BaseMixin):

    def test_detail_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(detail='full'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['detail'], 'full')  # noqa

    def test_default_detail_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(detail=DEFAULT_DETAIL))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('detail' not in actual)  # noqa

    def test_invalid_detail_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(detail='empty'))  # noqa
