from fxa.notes.db_notes_repository import DbNotesRepository
from fxa.preprocessing.preprocess import preprocess_document
from fxa.dictionaries.import_dictionaries import get_currencies_words
from fxa.dictionaries.import_dictionaries import get_prediction_notes
from fxa.config.db import get_session

from pprint import pprint
import operator


def process_words(processed_document, dict_words, dict_currencies):
    positive_words = 0
    negative_words = 0
    currencies_words = {}
    growth = None
    currency = None

    for word in processed_document:
        if word in dict_words:
            if dict_words[word] is True:
                positive_words += 1
            else:
                negative_words += 1

        if word in dict_currencies:
            if dict_currencies[word] in currencies_words:
                currencies_words[dict_currencies[word]] += 1
            else:
                currencies_words[dict_currencies[word]] = 1

    if positive_words > negative_words:
        growth = True
    elif positive_words == negative_words:
        growth = None
    else:
        growth = False

    if bool(currencies_words):
        sorted_currencies = sorted(currencies_words.items(), key=operator.itemgetter(1))
        currency = sorted_currencies[-1][0]

    return growth, currency



def main():
    pw_filename = 'fxa/dictionaries/dict_prediction.csv'
    cw_filename = 'fxa/dictionaries/dict_currencies.csv'


    for lang in ["pl", "es", "en", "fr"]:

        dict_currencies = get_currencies_words(lang, cw_filename)
        dict_words = get_prediction_notes(lang, pw_filename)

        notes_repository = DbNotesRepository()
        session, notes = notes_repository.get_notes_by_language_with_session(lang)

        for note in notes:
            pprint(lang)
            pprint(note.id)

            if note.content is None:
                continue

            processed_document = preprocess_document(note.content, lang)
            growth, currency = process_words(processed_document, dict_words, dict_currencies)

            note.growth = growth
            note.currency = currency

        session.commit()

if __name__ == '__main__':
    main()
