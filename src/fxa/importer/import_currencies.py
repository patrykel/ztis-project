from fxa.config.db import db_connect
from fxa.currencies.csv_currencies_repository import CsvCurrenciesRepository
from fxa.currencies.currency import Base, Currency
from sqlalchemy.orm import sessionmaker
from fxa.utils import parse_date


def import_currencies_single_csv(base_currency, currency, csv_filename):
    con, meta = db_connect()
    Base.metadata.create_all(con)
    Session = sessionmaker(bind=con)
    session = Session()
    currencies_repository = CsvCurrenciesRepository(
        base_currency, currency, csv_filename
    )
    rates = currencies_repository.get_rates()
    currencies = []
    for key, value in rates.items():
        currency_obj = Currency(
            date=parse_date(key),
            base_currency=base_currency,
            currency=currency,
            value=value['avg']
        )
        currencies.append(currency_obj)
    session.add_all(currencies)
    session.commit()
