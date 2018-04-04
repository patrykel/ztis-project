from nltk.stem.snowball import EnglishStemmer, FrenchStemmer, SpanishStemmer

STEMMERS = {
    "en": EnglishStemmer,
    "fr": FrenchStemmer,
    "es": SpanishStemmer,
}


class PolishStemmer(object):

    @classmethod
    def stem(cls, word):
        return word  # TODO: Add PLP support


def get_stemmer(lang):
    """ Returns a stemmer for a given language.

    @param lang Language code, e.g. "en"
    """
    if lang in STEMMERS:
        return STEMMERS[lang]()
    elif lang == "pl":
        return PolishStemmer()
    else:
        raise Exception("No Stemmer for lang {}".format(lang))
