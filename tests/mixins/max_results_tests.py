from tests.mixins import BaseMixin


class MaxResultsTestsMixin(BaseMixin):

    default = None

    def get_max_results_default(self):
        raise NotImplemented('You must implement get_max_results_default()')

    def test_max_results_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(max_results=1))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['maxResults'], 1)  # noqa

    def test_default_max_results_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(max_results=self.get_max_results_default()))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('maxResults' not in actual)  # noqa

    def test_invalid_max_results_raises_error(self, mocked_function):  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(max_results=0))  # noqa
        self.assertRaises(ValueError, self.get_fixture(), **self.get_params(max_results=10001))  # noqa
