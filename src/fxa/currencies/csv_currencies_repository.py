import pandas as pd


class CsvCurrenciesRepository:

    def __init__(self, base_currency, currency, filename):
        self.base_currency = base_currency
        self.currency = currency
        self.filename = filename
        self.rates = None

    def get_currency_rate(self, base, currency, date):
        if self.base_currency != base or self.currency != currency:
            return None
        self._read_rates()
        return self.rates[date]

    def get_rates(self):
        self._read_rates()
        return self.rates

    def _read_rates(self):
        if self.rates is not None:
            return
        currencies_data = pd.read_csv(self.filename, sep=';')
        currencies_data.columns = ['date', 'open',
                                   'high', 'low', 'close', 'volume']
        # Extract only date from first column
        currencies_data['date'] = currencies_data['date'].str.split(' ').str.get(0)
        currencies_data = currencies_data.groupby('date').mean()
        currencies_data['avg'] = (currencies_data['open'] + currencies_data['close']) / 2
        self.rates = currencies_data.to_dict(orient='index')
