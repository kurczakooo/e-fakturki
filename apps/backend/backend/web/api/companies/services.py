from babel import Locale

from backend.web.api.companies.schemas import IsoCountry

KSEF_SPECIFIC_COUNTRIES = {
    "AN": "Antyle Holenderskie",
    "XC": "Ceuta",
    "XL": "Melilla",
    "XI": "Zjednoczone Królestwo (Irlandia Północna)",
}


def get_polish_country_name(code: str) -> IsoCountry:
    """Get Polish name of the country based on country code."""
    locale = Locale("pl")
    if code in KSEF_SPECIFIC_COUNTRIES:
        return IsoCountry(name=KSEF_SPECIFIC_COUNTRIES[code], code=code)

    return IsoCountry(name=locale.territories.get(code, code), code=code)
