import time
import scrython

from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format
from sqlalchemy.exc import IntegrityError


from sqlalchemy import (MetaData, Table, Text)

class DBManager:
    def __init__(self, db, app, engine, metadata):
        self._db = db
        self._app = app
        self._engine = engine
        self._metadata = metadata

        self._model_map = {
            "cards": Card,
            "formats": Format
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
        try:
            self.db.session.add(entry)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()

    def add_single_card(self, search_term):
        item = scrython.cards.Search(q=search_term).data()[0]
        list = [item]
        self.cards_from_list(list, parse_legality=True, list_unknown_legalities=True)


    def cards_from_list(self, list, parse_legality=False, list_unknown_legalities=False):
        for sco in list:
            new_card = Card()
            self.db.session.add(new_card)
            new_card.parse_scrython_object(sco)
            new_card.determine_games_from_object(sco)
            if parse_legality:
                new_card.determine_legality_from_object(sco)
                if list_unknown_legalities:
                    self.list_unknown(new_card)
            self.add_entry(new_card)

    def cmc_gradient(self):
        #corresponds respectively to the number of printed cards of cmc 0, 1, 2, 3, 4, 5 and greater
        #used in assert testing for a mass download
        #will also need to be incorporated into any scheduled update routine, but for now can just
        #be declared.
        return [1299, 2932, 6198, 7104, 5620, 3549, 3165]

    def clear(self, table_name):
        table = self.fetch_table(table_name)
        items = table.query.all()
        for item in items:
            self.db.session.delete(item)
        self.db.session.commit()

    def download(self):
        grads = self.cmc_gradient()
        i = 0
        expected = 0
        while i <= 6:
            if i <= 5:
                cmc = str(i)
                comp = "="
            else:
                cmc = "5"
                comp = ">"
            try:
                expected += grads[i]
                search_term = (f"cmc{comp}{cmc} and game=paper")
                time.sleep(1)
                count = self.db.session.execute(Text("SELECT COUNT(_id) FROM cards"))
                if count != expected:
                    raise Exception(f"Expected {expected} but got {count}")
                else:
                    print(f"Downloaded cards where cmc{comp}{cmc}...")
                i += 1
            except Exception as e:
                print(f"Error where cmc{comp}{cmc}: {e}")
                break
        self.add_single_card("Little Girl")


    def drop_from_string(self, string):
        table = self.fetch_table(string)
        self.db.session.delete(table)
        self.db.session.commit()
        pass

    def fetch_table(self, string):
        return self.model_map.get(string)

    def list_unknown(self, sco):
        formats = self.db.session.query(Format).all()
        scryfall_names = []
        for format in formats:
            scryfall_names.append(format.scryfall_name)
        keys = list(sco['legalities'].keys())
        unknown = []
        for key in keys:
            if key not in scryfall_names:
                unknown.append(key)
        if len(unknown) > 0:
            print(f"Card {sco['name']} references the following unknown formats:")
            for u in unknown:
                print(f"\t{u}")

    def manage_cards(self,
                     drop=False,
                     clear=False,
                     mass_insert=False,
                     source=None,
                     parse_legality=False,
                     list_unknown_legalities=False):
        if drop:
            Card.__table__.drop(self._engine)
            Face.__table__.drop(self._engine)
        if clear:
            self.clear("cards")
        if mass_insert:
            if source is not None:
                self.cards_from_list(source, parse_legality, list_unknown_legalities)
            else:
                self.download()


    def manage_formats(self,
                       drop=False,
                       clear=False,
                       mass_insert=False,
                       source=None):
        if drop:
            Format.__table__.drop(self._engine)
        if clear:
            self.clear("formats")
        if mass_insert:
            if source is not None:
                self.objects_from_list(source)
            else:
                raise Exception("source is required")

    def manage_games(self,
                     drop=False,
                     clear=False,
                     mass_insert=False,
                     source=None):
        if drop:
            Format.__games__.drop(self._engine)
        if clear:
            self.clear("games")
        if mass_insert:
            if source is not None:
                self.objects_from_list(source)
            else:
                raise Exception("source is required")

    def objects_from_list(self, source):
        for item in source:
            self.add_entry(item)


    def lookup(self, search_term):
        more = True
        page = 1
        while more:
            result = scrython.cards.Search(q=search_term, page=page)
            for card in result.data():
                output = []
                tmp = card
                output.append(tmp)
                self.cards_from_list(output, parse_legality=True, list_unknown_legalities=True)
            more = result.has_more()
            page += 1
            time.sleep(0.5)








