import spacy


class MLAddressParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
