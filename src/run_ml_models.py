from fxa.currencies.db_currency_repository import DbCurrencyRepository
from fxa.notes.db_notes_repository import DbNotesRepository
from fxa.ml.predict_currency import run_ml_tests


def main():
    currency_repository = DbCurrencyRepository()
    notes_repository = DbNotesRepository()
    notes = notes_repository.get_notes_by_language("en")
    notes = notes[:50000]
    run_ml_tests(notes, currency_repository)


if __name__ == '__main__':
    main()
