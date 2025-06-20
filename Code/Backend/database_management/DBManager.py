import time
import scrython

from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face
from database_management.models.Format import Format
from database_management.models.Game import Game
from database_management.models.Intermediates import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List


from sqlalchemy import (MetaData, Table, text)

class DBManager:
    def __init__(self, db, app, engine, metadata):
        self._db = db
        self._app = app
        self._engine = engine
        self._metadata = metadata

        self._model_map = {
            "cards": Card,
            "faces": Face,
            "formats": Format,
            "cycles": Cycle,
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

    #SETUP FUNCTIONS

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

    def card_in_table(self, name):
        """        command = f"SELECT COUNT(*) FROM cards WHERE _name = \"{name}\""
        result = self.db.session.execute(text(command))
        tally = result.fetchone()[0]
        if tally != 0:
            return True
        else:
            return False"""
        return self.db.session.query(Card).filter(Card._name == name).count() > 0

    def cards_from_list(self, list, parse_legality=False, list_unknown_legalities=False):
        for sco in list:
            if not self.check_edge_case(sco):
                new_card = Card()
                new_card.parse_scrython_object(sco)
                self.db.session.add(new_card)
                self.db.session.flush()
                new_card.determine_games_from_object(sco)
                if parse_legality:
                    new_card.determine_legality_from_object(sco)
                    if list_unknown_legalities:
                        self.list_unknown(sco)
                self.add_entry(new_card)

    def card_from_table(self, name):
        command = select(Card).where(Card._name.in_([name]))
        result = self.db.session.scalars(command)
        return result.first()


    def check_edge_case(self, sco):
        edge_case = True
        unset_multiples = ["Ineffable Blessing",
                           "Knight of the Kitchen Sink",
                           "Sly Spy",
                           "Very Cryptic Command",
                           "Everythingamajig",
                           "Garbage Elemental"]
        if sco['name'] == 'B.F.M. (Big Furry Monster)' and self.card_in_table(sco['name']):
            self.edge_case_nonunique(sco, "bfm")
        elif sco['type_line'] == 'Artifact — Attraction' and self.card_in_table(sco['name']):
            self.edge_case_nonunique(sco, "multiple")
        elif sco['name'] in unset_multiples and self.card_in_table(sco['name']):
            self.edge_case_nonunique(sco, "multiple")
        elif sco['name'] == 'Little Girl':
            self.edge_case_little_girl(sco)
        else:
            edge_case = False
        return edge_case


    def clear(self, table_name):
        table = self.fetch_table(table_name)
        if table is None:
            raise Exception(f"Table '{table_name}' does not exist")
        items = table.query
        items.delete(synchronize_session=False)
        self.db.session.commit()

    def count_rows(self, table_name, condition = None, context = False):
        command = self.where_statement("SELECT COUNT(*) FROM " + table_name, condition)
        result = self.db_execute(text(command), context)
        output = result.fetchone()[0]
        if not isinstance(output, int):
            raise Exception(f"Received {output} from {table_name} when counting rows")
        else:
            return output

    def edge_case_little_girl(self, sco):
        sco["cmc"] = 1
        lg = Card()
        lg.parse_scrython_object(sco)

        self.db.session.add(lg)
        self.db.session.flush()
        lg.determine_games_from_object(sco)
        lg.determine_legality_from_object(sco)
        self.list_unknown(sco)
        self.add_entry(lg)


    def edge_case_nonunique(self, sco, layout):
        card = self.card_from_table(sco['name'])
        card.add_face_manually(sco)
        card.layout = layout
        self.db.session.commit()

    def fix_card_multiples(self):
        pass

    def fix_cards(self):
        self.fix_card_multiples()
        self.fix_omens()

    def fix_omens(self):
        statement = select(Card).join(Card.faces).where(Face.type)

    def get_card_information(self,
                             run = False,
                             source = None,
                             subsect = "legalities"):
        if run:
            sample = source[0][subsect]
            for item in sample:
                print (item)



    def download(self, start):
        i = start
        while i <= 6:
            if i <= 5:
                cmc = str(i)
                comp = "="
            else:
                cmc = "5"
                comp = ">"
            try:
                search_term = (f"cmc{comp}{cmc} and game=paper")
                self.lookup(search_term)
                time.sleep(1)
                print(f"Downloaded cards where cmc{comp}{cmc}...")
                quant = self.count_rows("cards", f"_cmc{comp}{cmc}")
                print(f"Table contains {quant} cards of that description")
                i += 1
            except Exception as e:
                print(f"Error where cmc{comp}{cmc}: {e}")
                break
        self.add_single_card("Little Girl")

    def download_to_file(self):
        more = True
        page = 1
        with open("database_management/fillscripts/AllCards.py", "w") as all_cards:
            all_cards.seek(0)
            all_cards.truncate()
            all_cards.write("all_cards = [")
        while more:
            output = []
            #(game:paper)
            result = scrython.cards.Search(q="(game:paper)", page=page)
            for card in result.data():
                output.append(card)
            print("Batch downloaded for page " + str(page))
            for item in output:
                with open("database_management/fillscripts/AllCards.py", "a") as all_cards:
                    all_cards.write("\n")
                    all_cards.write(str(item) + ",")
            print("Added to file for page " + str(page))
            more = result.has_more()
            page += 1
            time.sleep(0.2)
            print("")
        with open("database_management/fillscripts/AllCards.py", "a") as all_cards:
            all_cards.write("]")

    def drop_from_string(self, string):
        table = self.fetch_table(string)
        self.db.session.delete(table)
        self.db.session.commit()
        pass

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
                     list_unknown_legalities=False,
                     set_lands = False,
                     only_lands = True):
        if drop:
            Card.__table__.drop(self._engine)
            Face.__table__.drop(self._engine)
            Banned.__table__.drop(self._engine)
            Restricted.__table__.drop(self._engine)
            Legal.__table__.drop(self._engine)
            GameCards.__table__.drop(self._engine)
        if clear:
            self.clear("cards")
        if mass_insert:
            if not isinstance(source, int):
                self.cards_from_list(source, parse_legality, list_unknown_legalities)
            else:
                self.download(source)
        if set_lands:
            self.set_cycles(lands=only_lands)

    def manage_cycles(self,
                       drop=False,
                       clear=False,
                       mass_insert=False,
                       source=None,
                       reset_cards=False):
        if drop:
            Cycle.__table__.drop(self._engine)
        if clear:
            self.clear("cycles")
        if mass_insert:
            if source is not None:
                self.objects_from_list(source)
            else:
                raise Exception("source is required")
        if reset_cards:
            self.set_cycles(reset=True, lands=False)

    def manage_formats(self,
                       drop=False,
                       clear=False,
                       mass_insert=False,
                       source=None):
        if drop:
            Format.__table__.drop(self._engine)
            GameFormats.__table__.drop(self._engine)
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
            Game.__table__.drop(self._engine)
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

    def run_join(self, t):
        pass

    def set_cycles(self, reset=False, lands=True):
        statement = select(Card)
        if lands:
            results = self.db.session.query(Card).filter(Card._overall_land).all()
        else:
            results = self.db.session.query(Card).all()
        #results = self.db_scalars(statement)
        if reset:
            for card in results:
                card.reset_cycle()
        else:
            for card in results:
                card.determine_cycle()
        self.db.session.commit()

    def where_statement(self, command, condition = None):
        if condition is None:
            return command
        if not isinstance(condition, str):
            raise Exception(f"where_statement: condition for command {command} must be str")
        else:
            new_command = command + " WHERE " + condition
            return new_command


    #STATEMENT GRAMMAR FUNCTIONS
    def fetch_attribute(self, key, table):
        match key:
            case "card_id":
                return table._card_id
            case "id":
                return table._id
            case "name":
                return table._name
            case _:
                raise Exception(f"[ERROR] no match for proposed attribute {key}")

    def isolate(self, results, expect_single):
        if expect_single:
            output = results.first()
            return results.first()
        else:
            return results.all()


    #ACCESS FUNCTIONS
    def all_entries(self, table_name, context=False):
        table = self.fetch_table(table_name)
        if context:
            with self.app.app_context():
                output = self.db.session.query(table).all()
        else:
            output = self.db.session.query(table).all()
        return output;


    def db_execute(self, statement, context=False):
        if context:
            with self.app.app_context():
                return self.db.session.execute(statement)
        else:
            return self.db.session.execute(statement)

    def db_scalars(self, statement, expect_single = True, context=False):
        if context:
            with self.app.app_context():
                result = self.db.session.scalars(statement)
                return self.isolate(result, expect_single)
        else:
            result = self.db.session.scalars(statement)
            return self.isolate(result, expect_single)

    def fetch_table(self, string):
        return self.model_map.get(string)

    def key_lookup(self, term, tablename, key, expect_single=True, context=False):
        x = 3
        table = self.fetch_table(tablename)
        attribute = self.fetch_attribute(key, table)

        if context:
            with self.app.app_context():
                result = self.db.session.query(table).filter(attribute == term)
                return self.isolate(result, expect_single)
        else:
            result = self.db.session.query(table).filter(attribute == term)
            return self.isolate(result, expect_single)


"""        if expect_single:
            return result.one()
        else:
            return result
"""








