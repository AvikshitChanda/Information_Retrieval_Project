import string
def normalize_punctuation(text):
    text = text.translate(str.maketrans("", "", string.punctuation.replace("-", "").replace(".", "")))
    # Remove dots within words but preserve decimal points and email addresses
    text = re.sub(r'\b(\w(?:\.\w)+)\b', lambda x: x.group(1).replace('.', ''), text)

    return text