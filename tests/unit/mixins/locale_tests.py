from ebird.api.requests.constants import DEFAULT_LOCALE
from tests.unit.mixins.base import BaseMixin


class LocaleTestsMixin(BaseMixin):
    def test_locale_is_sent(self):
        query = self.api_call(locale="fr")[1]
        self.assertEqual(query["locale"], "fr")

    def test_default_locale_is_not_sent(self):
        query = self.api_call(locale=DEFAULT_LOCALE)[1]
        self.assertTrue("locale" not in query)


class SpeciesLocaleTestsMixin(BaseMixin):
    def test_locale_is_sent(self):
        query = self.api_call(locale="fr")[1]
        self.assertEqual(query["sppLocale"], "fr")

    def test_default_locale_is_not_sent(self):
        query = self.api_call(locale=DEFAULT_LOCALE)[1]
        self.assertTrue("sppLocale" not in query)


class GroupLocaleTestsMixin(BaseMixin):
    def test_locale_is_sent(self):
        query = self.api_call(locale="fr")[1]
        self.assertEqual(query["groupNameLocale"], "fr")

    def test_default_locale_is_not_sent(self):
        query = self.api_call(locale=DEFAULT_LOCALE)[1]
        self.assertTrue("groupNameLocale" not in query)
