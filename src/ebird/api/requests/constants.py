"""Various constants and values used in the API."""

DEFAULT_BACK = 14
DEFAULT_DETAIL = "simple"
DEFAULT_DISTANCE = 25
DEFAULT_HOTSPOTS_ONLY = "false"
DEFAULT_PROVISIONAL = "false"
DEFAULT_LOCALE = "en"
DEFAULT_OBSERVATION_ORDER = "date"
DEFAULT_SPECIES_CATEGORY = None
DEFAULT_TAXONOMY_ORDER = "ebird"
DEFAULT_MAX_OBSERVATIONS = None
DEFAULT_MAX_OBSERVERS = 100
DEFAULT_MAX_CHECKLISTS = 10
DEFAULT_TOP_100_RANK = "spp"

API_MAX_RESULTS = 200

LOCALES = {
    "Bulgarian": "bg",
    "Chinese": "zh",
    "Chinese (Simple)": "zh_SIM",
    "Croatian": "hr",
    "Czech": "cs",
    "Dutch": "nl",
    "Danish": "da",
    "English": "en",
    "English (Australia)": "en_AU",
    "English (India)": "en_IN",
    "English (IOC)": "en_IOC",
    "English (Hawaii)": "en_HAW",
    "English (Kenya)": "en_KE",
    "English (Malaysia)": "en_MY",
    "English (New Zealand)": "en_NZ",
    "English (Philippines)": "en_PH",
    "English (South Africa)": "en_ZA",
    "English (United Arab Emirates)": "en_AE",
    "English (Great Britain)": "en_UK",
    "English (United States)": "en_US",
    "Faroese": "fo",
    "Finnish": "fi",
    "French": "fr",
    "French (AOU)": "fr_AOU",
    "French (Canada)": "fr_CA",
    "German": "de",
    "French (Guadeloupe)": "fr_GP",
    "French (Haiti)": "fr_HT",
    "Haitian": "ht_HT",
    "Hebrew": "iw",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Icelandic": "is",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malayalam": "ml",
    "Mongolian": "mn",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese (Portugal)": "pt_PT",
    "Portuguese (Brasil)": "pt_BR",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovenian": "sl",
    "Spanish": "es",
    "Spanish (Argentina)": "es_AR",
    "Spanish (Chile)": "es_CL",
    "Spanish (Costa Rica)": "es_CR",
    "Spanish (Cuba)": "es_CU",
    "Spanish (Dominican Republic)": "es_DO",
    "Spanish (Ecuador)": "es_EC",
    "Spanish (Spain)": "es_ES",
    "Spanish (Mexico)": "es_MX",
    "Spanish (Panama)": "es_PA",
    "Spanish (Puerto Rico)": "es_PR",
    "Spanish (Uruguay)": "es_UY",
    "Spanish (Venezuela)": "es_VE",
    "Swedish": "sv",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
}

SPECIES_CATEGORIES = [
    "domestic",
    "form",
    "hybrid",
    "intergrade",
    "issf",
    "slash",
    "species",
    "spuh",
]

SPECIES_ORDERING = ["ebird", "merlin"]

SPECIES_SORT = ["date", "species"]

REGION_TYPES = ["country", "subnational1", "subnational2"]

TOP_100_RANK = ["spp", "cl"]

# Just occasionally the connection to eBird freezes. The timeout
# will raise an error which is preferable to the sitting there
# waiting for something to happen, when it will not.
DEFAULT_TIMEOUT = 30
