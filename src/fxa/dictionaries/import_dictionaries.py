import csv

def get_currencies_words(lang, filename):
    """
    Returns dictionary with currencies names in specified language
    """

    words = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=",")
        for line in reader:
            if line['language'] == lang:
                words[line['code']] = line['code']
                words[line['unit_text']] = line['code']
                words[line['symbol']] = line['code']
    return words

def get_prediction_notes(lang, filename):
    """
    Returns dictionary with words associated with growth
    or deprecation of currency in specified language
    """

    words = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=",")
        for line in reader:
            if line['language'] == lang:
                words[line['word']] = __string_to_boolean(line['positive'])
    return words

def __string_to_boolean(str):
    return True if str == 'true' else False
