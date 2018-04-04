from fxa.config.db import db_connect
from pandas import read_sql_table


LANGS = [
    "pl",
    "en",
    "es",
    "fr",
]


def notes_count(notes):
    count = len(notes)
    print("Ilość notatek w bazie danych:", count)


def notes_count_by_lang(notes):
    for lang in LANGS:
        lang_notes = notes[notes['feed'].str.startswith(lang)]
        print("Ilość notatek w języku {}".format(lang), len(lang_notes))


def notes_by_currencies(notes):
    currencies = set(filter(None.__ne__, notes['currency']))
    for currency in currencies:
        currency_notes = notes[notes['currency'] == currency]
        print("Ilość notatek o walucie {}".format(currency),
              len(currency_notes))


def notes_by_growth(notes):
    growths = set(filter(None.__ne__, notes['growth']))
    for growth in growths:
        growth_notes = notes[notes['growth'] == growth]
        print("Ilość notatek mówiąca o wzroście {}".format(growth),
              len(growth_notes))


def overall_stats(notes):
    notes_count(notes)
    notes_count_by_lang(notes)
    notes_by_currencies(notes)
    notes_by_growth(notes)


def main():
    con, _ = db_connect()
    notes = read_sql_table('notes', con)
    overall_stats(notes)
    for lang in LANGS:
        print("Analiza notatek w języku {}".format(lang))
        lang_notes = notes[notes['feed'].str.startswith(lang)]
        notes_by_currencies(lang_notes)
        notes_by_growth(lang_notes)

if __name__ == '__main__':
    main()
