from fxa.config.db import get_session
from fxa.currencies.currency import Currency
from sqlalchemy import and_


class DbCurrencyRepository:

    def get_currency_rate(self, base, currency, date):
        session = get_session()
        return session.query(Currency) \
            .filter(and_(
                Currency.base_currency == base,
                Currency.currency == currency,
                Currency.date == date
            )) \
            .first()
