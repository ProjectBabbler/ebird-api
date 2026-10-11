from ebird.api.requests import get_taxonomy_locales


def test_api_call(api_token):
    locales = get_taxonomy_locales(api_token)
    assert "en" in [locale["code"] for locale in locales]
