from database_management.models.Card import Card

from sqlalchemy import (MetaData, Table)

class DBManager:
    def __init__(self, db, app, engine, metadata):
        self._db = db
        self._app = app
        self._engine = engine
        self._metadata = metadata

        self._model_map = {
            "cards": Card
        }



#getters and setters
    @property
    def db(self):
        return self._db

    @property
    def app(self):
        return self._app

    @property
    def engine(self):
        return self._engine

    @property
    def metadata(self):
        return self._metadata

    @property
    def model_map(self):
        return self._model_map

    #useful functions

    def add_entry(self, entry):
        self.db.session.add(entry)
        self.db.session.commit()

    def cards_from_list(self, list):
        for sco in list:
            new_card = Card()
            new_card.parse_scrython_object(sco)
            self.add_entry(new_card)




    def manage_cards(self,
                     drop=False,
                     clear=False,
                     mass_insert=False,
                     source=None):
        if drop:
            pass
        if clear:
            self.clear("cards")
        if mass_insert:
            if source is not None:
                self.cards_from_list(source)
            else:
                self.download()



    def clear(self, table_name):
        table = self.model_map.get(table_name)
        items = table.query.all()
        for item in items:
            self.db.session.delete(item)
        self.db.session.commit()





