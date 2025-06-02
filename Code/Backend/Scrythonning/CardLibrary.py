import scrython
import asyncio
import numpy
import time

import CustomExceptions

from Card import Card

#prices': {'usd': '0.07', 'usd_foil': '0.64', 'usd_etched':
"""result = scrython.cards.Search(q='sidisi')
print(str(result.total_cards()) + " cards:")
for card in result.data():
    print("card: " + card['name'])
    print("cmc: " + card['mana_cost'])
    print("price: " + card['prices']['usd'])
    print("object: " + str(card))"""

class CardLibrary:
    def __init__(self):
        self.supertypes = ["Basic", "Legendary", "Ongoing", "Snow", "World"]

    def extract_single_card(self, result, search_term):
        for card in result.data():
            sp = card['name'].split(" // ")
            if search_term in sp:
                print(card["prices"])
                return card
        raise CustomExceptions.CardNotFound(search_term)

    def format_double_faced_cards(self, one, two):
        oracle_text_1 = one['oracle_text']  # bad double
        cmc_1 = one['mana_cost']

        oracle_text_2 = two['oracle_text']
        cmc_2 = two['mana_cost']

        tl1 = self.parse_type_line(one["type_line"])
        tl2 = self.parse_type_line(two["type_line"])



        ot = oracle_text_1 + " // " + oracle_text_2
        cmc = cmc_1 + " // " + cmc_2


        supertypes = set(tl1["supertypes"] + tl2["supertypes"])
        types = set(tl1["types"] + tl2["types"])
        subtypes = set(tl1["subtypes"] + tl2["subtypes"])


        return {
            "oracle_text":ot,
            "cmc":cmc,
            "supertypes":supertypes,
            "types":types,
            "subtypes":subtypes
        }


    def get_card_details(self, card):
        name = card['name']
        color_identity = card['color_identity']
        price = card['prices']['usd']
        legality = card['legalities']
        games = card['games']
        release_date = card['released_at']

        type_line = card['type_line']
        parsed = self.parse_type_line(type_line)
        supertypes = parsed['supertypes']
        types = parsed['types']
        subtypes = parsed['subtypes']

        return {
            "name":name,
            "color_identity":color_identity,
            "price":price,
            "legality":legality,
            "games":games,
            "supertypes":supertypes,
            "types":types,
            "subtypes":subtypes,
            "release_date":release_date
        }

    def lookup(self, search_term):
        result = scrython.cards.Search(q=search_term)
        return result


    def lookup_by_name(self, search_term):
        try:
            # Manually set up event loop if none exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            result = scrython.cards.Search(q=search_term)
            card = self.extract_single_card(result, search_term)
            return self.parse_scrython_object(card)

        except Exception as e:
            print("Error during card fetch:", e)
            raise

    def lookup_by_type(self, search_term):
        try:
            # Manually set up event loop if none exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            try:
                output = []
                more = True
                page = 1
                while more:
                    result = scrython.cards.Search(q=search_term, page=page)
                    print(result.total_cards())
                    for card in result.data():
                        tmp = self.parse_scrython_object(card)
                        output.append(tmp)
                    print("LAST ITEM: " + output[-1].name)
                    more = result.has_more()
                    page += 1
                    time.sleep(0.1)
                return output
            except Exception as e:
                print(e)
                return ""
        except Exception as e:
            print("Error during card fetch:", e)
            raise


    def parse_scrython_object(self, card):

        """
        for element in card:
            tag = element
            content = card[element]
            print(tag)
            print(content)
            print("")"""

        details = self.get_card_details(card)

        name = details['name']
        color_identity = details['color_identity'] #Throws Error
        price = details['price'] #Throws error
        legality = details['legality']
        games = details['games']
        release_date = details['release_date']

        try:
            supertypes = details['supertypes']
            types = details['types']
            subtypes = details['subtypes']
            oracle_text = card['oracle_text'] #bad double
            cmc = card['mana_cost'] #bad double
            return Card(name, cmc, color_identity, price, supertypes, types, subtypes, oracle_text, legality, games, release_date)
        except Exception as e:
            faces = card['card_faces']
            formatted_details = self.format_double_faced_cards(faces[0], faces[1])
            oracle_text = formatted_details["oracle_text"]
            cmc = formatted_details["cmc"]
            supertypes = formatted_details['supertypes']
            types = formatted_details['types']
            subtypes = formatted_details['subtypes']
            return Card(name, cmc, color_identity, price, supertypes, types, subtypes, oracle_text, legality, games, release_date)




    def parse_type_line(self, tl):
        supertypes = []
        types = []
        subtypes = []


        space_split = tl.split(" ")
        while space_split[0] in self.supertypes:
            supertypes.append(space_split.pop(0))


        while len(space_split) > 0 and space_split[0] != "—":
            types.append(space_split.pop(0))


        if len(space_split) != 0:
            space_split.pop(0)
            subtypes = space_split

        return {"supertypes":supertypes, "types":types, "subtypes":subtypes}






