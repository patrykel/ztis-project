import argparse
from fxa.notes.db_notes_repository import DbNotesRepository
from fxa.preprocessing.make_doc2vec_model import make_doc2vec_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lang',
                        action='store',
                        required=True,
                        help='Language for doc2vec model.')
    parser.add_argument('-o', '--out',
                        action='store',
                        required=True,
                        help='Output model filename.')

    args = parser.parse_args()

    lang = args.lang
    notes_repository = DbNotesRepository()
    notes = notes_repository.get_notes_by_language(lang)
    model = make_doc2vec_model(notes, lang)
    model.save(args.out)


if __name__ == "__main__":
    main()
