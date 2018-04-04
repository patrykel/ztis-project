from gensim.models.doc2vec import Doc2Vec

MODELS_BASE_DIR = "data/models/"

DOC2VEC_MODELS = {
    "en": Doc2Vec.load(MODELS_BASE_DIR + "english/english.model"),
    "es": Doc2Vec.load(MODELS_BASE_DIR + "spanish/spanish.model"),
    "fr": Doc2Vec.load(MODELS_BASE_DIR + "french/french.model"),
    "pl": Doc2Vec.load(MODELS_BASE_DIR + "polish/polish.model"),
}


def load_model(lang):
    model = DOC2VEC_MODELS[lang]
    return model
