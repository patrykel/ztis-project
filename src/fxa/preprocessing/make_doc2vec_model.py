from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from fxa.preprocessing.preprocess import preprocess_document


def prepare_note(note, lang):
    words = preprocess_document(note.content, lang)
    return TaggedDocument(words=words, tags=[note.id])


def make_doc2vec_model(notes, lang):
    documents = [prepare_note(note, lang) for note in notes]
    documents = list(filter(lambda doc: doc.words is not None, documents))
    model = Doc2Vec(min_count=1, size=100)
    model.build_vocab(documents)
    model.train(documents, total_examples=len(notes), epochs=100)
    return model
