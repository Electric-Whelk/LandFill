class CardNotFound(Exception):
    def __init__self(self, search_term):
        self._search_term = search_term

    @property
    def search_term(self):
        return self._search_term
