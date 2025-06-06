class CardNotFound(Exception):
    def __init__self(self, search_term):
        self._search_term = search_term

    @property
    def search_term(self):
        return self._search_term

class Messenger(Exception):
    def __init__(self, code):
        self._code = 1

    @property
    def code(self):
        return self._code
