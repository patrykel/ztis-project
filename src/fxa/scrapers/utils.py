EXTRA_CHARS = [
    '\n',
    '\r',
    '\t',
]

def clean(text):
    if text is None:
        return text
    for extra_char in EXTRA_CHARS:
        text = text.replace(extra_char, '')
    return text.strip()
