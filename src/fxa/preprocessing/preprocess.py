from nltk.tokenize import word_tokenize
from fxa.preprocessing.stopwords_provider import get_stopwords
from fxa.preprocessing.stemmer_provider import get_stemmer
import string

translator = str.maketrans('', '', string.punctuation)


def __remove_punctuation(text):
    return text.translate(translator)


def __remove_stopwords(words, lang):
    stopword_list = get_stopwords(lang)
    return [word for word in words if word not in stopword_list]


def __stem(words, lang):
    stemmer = get_stemmer(lang)
    return [stemmer.stem(word) for word in words]


def preprocess_document(text, lang):
    if not text:
        return

    text = __remove_punctuation(text)
    words = word_tokenize(text)
    words = __remove_stopwords(words, lang)
    stemmed = __stem(words, lang)
    return stemmed
