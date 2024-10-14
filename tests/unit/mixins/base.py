from unittest import mock


def get_response(url, params, headers):  # noqa
    return b"[]"


class BaseMixin:
    def assertTrue(self, expression, msg=None):
        raise NotImplementedError("TestCase must come before mixins")

    def assertEqual(self, first, second, msg=None):
        raise NotImplementedError("TestCase must come before mixins")

    def assertRaises(self, exception, callable, *args, **kwargs):  # noqa
        raise NotImplementedError("TestCase must come before mixins")

    def get_callable(self):
        raise NotImplementedError("You must define the API function to be tested")

    def get_params(self, **kwargs):
        return kwargs

    def api_call(self, **kwargs):
        with mock.patch("ebird.api.utils.get_response", side_effect=get_response) as fn:
            self.get_callable()(**self.get_params(**kwargs))
            args = fn.call_args[0]
            return args[0], args[1], args[2]  # url, params, headers

    def api_raises(self, exception, **kwargs):
        self.assertRaises(exception, self.get_callable(), **self.get_params(**kwargs))
