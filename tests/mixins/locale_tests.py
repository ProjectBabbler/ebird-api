from ebird.api.constants import DEFAULT_LOCALE
from tests.mixins import BaseMixin


class LocaleTestsMixin(BaseMixin):

    def test_locale_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale='fr'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['locale'], 'fr')  # noqa

    def test_default_locale_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale=DEFAULT_LOCALE))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('locale' not in actual)  # noqa


class SpeciesLocaleTestsMixin(BaseMixin):

    def test_locale_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale='fr'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['sppLocale'], 'fr')  # noqa

    def test_default_locale_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale=DEFAULT_LOCALE))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('sppLocale' not in actual)  # noqa


class GroupLocaleTestsMixin(BaseMixin):

    def test_locale_is_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale='fr'))
        actual = mocked_function.call_args[0][1]
        self.assertEqual(actual['groupNameLocale'], 'fr')  # noqa

    def test_default_locale_is_not_sent(self, mocked_function):
        self.get_fixture()(**self.get_params(locale=DEFAULT_LOCALE))
        actual = mocked_function.call_args[0][1]
        self.assertTrue('groupNameLocale' not in actual)  # noqa
