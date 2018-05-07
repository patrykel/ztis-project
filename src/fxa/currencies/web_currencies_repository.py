import requests
from fxa.utils import parse_date
from datetime import *

BASE_URL = 'http://api.fixer.io'


def get_url(base_currency, currency, date):
    return "%s/%d-%02d-%02d?base=%s&symbols=%s" % (
        BASE_URL,
        date.year,
        date.month,
        date.day,
        base_currency.upper(),
        currency.upper()
    )


class WebCurrenciesRepository:

    def __init__(self):
        pass

    def get_currency_rate(self, base_currency, currency, date):
        # url = get_url(base_currency, currency, parse_date(date))
        url = get_url(base_currency, currency, date)
        response = requests.get(url)
        return response.json()['rates'][currency.upper()]
