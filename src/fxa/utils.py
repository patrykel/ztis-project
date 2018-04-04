from fxa.preprocessing.doc2vec import load_model
import datetime


def parse_date(date):
    return datetime.datetime.strptime(date, '%Y%m%d')


def note_to_vec(note):
    note_lang = note.get_lang()
    doc2vec_model = load_model(note_lang)
    return doc2vec_model.docvecs[note.id]
