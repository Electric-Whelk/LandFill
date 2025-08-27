import time

from urllib.parse import quote_plus

from currency_converter import CurrencyConverter

from database_management.models.Card import Card
from database_management.models.Face import Face
from Extensions import db
from random import shuffle

from simulation_objects.GameCards import CommandTower, BondLand, DualLand, BattleLand, FastLand, SlowLand, PainLand, \
    HorizonLand, ArtifactTapLand, BicycleLand, ScryLand, TypedDualLand, GainLand
from simulation_objects.GameCards.TappedCycles.SurveilLand import SurveilLand

from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.ChoiceLands import DualFacedLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.MiscLand import MiscLand
from simulation_objects.GameCards.PermaUntapped import OGDualLand
from simulation_objects.GameCards.PermaUntapped.Verge import Verge
from simulation_objects.GameCards.SearchLands import SearchLand
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.PermaUntapped.FilterLand import FilterLand
from simulation_objects.GameCards.TappedCycles.GuildGate import GuildGate
from simulation_objects.GameCards.TappedCycles.TriTap import TriTap
from simulation_objects.GameCards.UntappableCycles.RevealLand import RevealLand
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.GameCards.TappedCycles.Triome import Triome
from simulation_objects.GameCards.UntappableCycles.CheckLand import CheckLand
from simulation_objects.GameCards.UntappableCycles.ShockLand import ShockLand
from simulation_objects.Misc.ColorPie import landtype_map


import os
import requests
from urllib.parse import quote


class CardCollection:
    def __init__(self):
        self._cards = []
        self._image_dir = os.path.expanduser("~/FinalProject/Code/Backend/card-images")

    #getters and setters
    @property
    def image_dir(self):
        return self._image_dir

    
    @property
    def card_list(self) -> list[GameCard]:
        return self._cards
    @card_list.setter
    def card_list(self, cards: list[GameCard]):
        self._cards = cards

    def length(self):
        return len(self.card_list)



    #sublists
    def lands_list(self, exclude = None) -> list[Land]:
        if exclude == None:
            return [x for x in self.card_list if isinstance(x, Land)]
        else:
            return [x for x in self.card_list if isinstance(x, Land) and x not in exclude]

    def landtypes_list(self):
        output = []
        for card in self.card_list:
            if isinstance(card, Land):
                output.extend(card.landtypes)
        return output

    def spells_list(self) -> list[Spell]:
        return [x for x in self.card_list if isinstance(x, Spell)]

    #card shifting
    def give(self, recipient:"CardCollection", item:GameCard):
        recipient.receive(item)
        self.card_list.remove(item)

    def give_all(self, recipient:"CardCollection"):
        cl = [c for c in self.card_list]
        for item in cl:
            self.give(recipient, item)

    def give_top(self, recipient:"CardCollection"):
        self.give(recipient, self.card_list[0])

    def receive(self, item:GameCard):
        self.card_list.append(item)

    def shuffle(self):
        shuffle(self.card_list)

    #cards used to add new GameCard objects


    def get_card_by_name(self, name) -> Card:
        edge_cases = {
            "Song of Earendil": "Song of Eärendil"
        }
        try:
            name = edge_cases[name]
        except KeyError:
            name = name

        try:
            face = db.session.query(Face).filter(Face._name == name).first()
            card = db.session.query(Card).filter(Card._id == face.card_id).first()
            return card
        except AttributeError:
            raise Exception(f"Could not find card {name}")


    def get_basic_spread(self):
        found = []
        output = []
        for card in self.card_list:
            if isinstance(card, BasicLand) and card.name not in [found] and card.name != self.last_worst:
                found.append(card.name)
                output.append(card)
        return output





    def parse_cards_from_json(self, cards):
        as_list = cards.split("\n")
        output = []
        for name in as_list:
            card = self.get_card_by_name(name)
            output.append(card)
        return output

    def set_card_list_from_ORM(self, cards:list[Card], mandatory=False):
        self.card_list = [self.parse_GameCard(x, mandatory) for x in cards]






    def parse_GameCard(self, card:Card, mandatory=False, commander=False):
        if not card.overall_land:
            return Spell(card, mandatory, commander=commander)
        else:
            cycle = card.cycle
            text = card.text
            name = cycle.name
            match name:
                case "Basic Lands":
                    return BasicLand(card, mandatory)
                case "Fetch Lands":
                    return FetchLand(card, mandatory)
                case "Bond Lands":
                    return BondLand(card, mandatory)
                case "Dual Lands":
                    return DualLand(card, mandatory)
                case "Battle Lands":
                    return BattleLand(card, mandatory)
                case "Fast Lands":
                    return FastLand(card, mandatory)
                case "Slow Lands":
                    return SlowLand(card, mandatory)
                case "Pain Lands":
                    return PainLand(card, mandatory)
                case "Horizon Lands":
                    return HorizonLand(card, mandatory)
                case "Shock Lands":
                    return ShockLand(card, mandatory)
                case "Triomes":
                    return Triome(card, mandatory)
                case "Tri-Color Taplands":
                    return TriTap(card, mandatory)
                case "Guildgates":
                    return GuildGate(card, mandatory)
                case "Filter Lands":
                    return FilterLand(card, mandatory)
                case "Verge Lands":
                    return Verge(card, mandatory)
                case "Check Lands":
                    return CheckLand(card, mandatory)
                case "Reveal Lands":
                    return RevealLand(card, mandatory)
                case "Dual Faced Lands":
                    return DualFacedLand(card, mandatory)
                case "OG Dual Lands":
                    return OGDualLand(card, mandatory)
                case "Surveil Lands":
                    return SurveilLand(card, mandatory)
                case "Artifact Taplands":
                    return ArtifactTapLand(card, mandatory)
                case "Bicycle Lands":
                    return BicycleLand(card, mandatory)
                case "Scry Lands":
                    return ScryLand(card, mandatory)
                case "Typed Dual Lands":
                    return TypedDualLand(card, mandatory)
                case "Gain Lands":
                    return GainLand(card, mandatory)

                #case "Bounce Lands":
                    #return BounceLand(card)
                case _:
                    return self.parse_land_by_name(card, mandatory)

    def parse_land_by_category(self, card, mandatory):
        untapped_duals = [
            "Bond Lands",
            "OG Dual Lands"
        ]
        tapped_duals = [
            "Artifact Taplands",
            "Bicycle Lands",
            "Gain Lands",
            "Guildgates",
        ]

    def parse_land_by_name(self, card:Card, mandatory):
        name = card.name
        match name:
            case "Command Tower":
                return CommandTower(card, mandatory)
            case _:
                return MiscLand(card, mandatory)

    def print_all(self):
        i = 0
        for card in self.permitted_lands():
            print(f"{i}: {card.name} ({card.fetchable})")
            i += 1

    def export_cards(self):
        return [card.to_dict() for card in self.card_list]

    def export_cycles(self):
        output = {}
        for card in self.card_list:
            if isinstance(card, Land) and not isinstance(card, BasicLand):
                if card.image is None:
                    card.image = self.get_cached_card_image_v2(card.name)
                usd = card.usd
                sp = self.sample_pound
                card.gbp = usd * sp
                try:
                    output[type(card).__name__]["cards"].append(card.to_dict())
                except KeyError:
                    output[type(card).__name__] = {
                        "typeName": type(card).__name__,
                        "cards": [card.to_dict()],
                        "displayName": card.cycle_display_name,
                        "alwaysTapped": card.permatap,
                        "fetchable": card.fetchable,
                        "altText": f"EXAMPLE: {card.name} - {card.text}"
                        #"maxPriceInDollars": card.usd,
                        #"maxPriceInEuros": card.eur,
                        #"maxPriceInGBP": card.gbp
                    }
            true_output = []
            for key in output:
                true_output.append(output[key])


        return true_output

    def get_cached_card_image_v2(self, card_name):

        #IMAGE_DIR = os.path.expanduser("~/FinalProject/Code/Backend/card-images")
        IMAGE_DIR = self.image_dir
        os.makedirs(IMAGE_DIR, exist_ok=True)
        """Return a URL to the card image, caching it if needed."""
        safe_name = card_name.replace(" ", "_").replace("/", "_") + ".jpg"
        file_path = os.path.join(IMAGE_DIR, safe_name)

        # If we don't already have the file, download it
        time.sleep(0.1)
        if not os.path.exists(file_path):

            print(f"Downloading image for {card_name} to {file_path}...")
            scryfall_url = f"https://api.scryfall.com/cards/named?exact={quote_plus(card_name)}"
            res = requests.get(scryfall_url)
            if res.status_code == 200:
                data = res.json()
                image_url = data.get("image_uris", {}).get("normal")
                if image_url:
                    img_res = requests.get(image_url)
                    if img_res.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(img_res.content)
            else:
                print(f"Failed to get Scryfall data for {card_name}")

        # Return the frontend-friendly URL
        return f"/card-images/{safe_name}"


    def get_cached_card_image(self, card_name):
        print(f"Getting image for {card_name}")
        """
        Fetches a card image from cache if available, otherwise from Scryfall.
        Saves to ~/FinalProject/Code/Backend/card-images/ and returns the file path.
        """
        # Expand the ~ to the absolute home path
        IMAGE_DIR = os.path.expanduser("~/FinalProject/Code/Backend/card-images")

        # Make sure the directory exists
        os.makedirs(IMAGE_DIR, exist_ok=True)

        # Make a safe filename
        safe_name = card_name.replace("/", "-").replace(" ", "_")
        file_path = os.path.join(IMAGE_DIR, f"{safe_name}.jpg")

        # If file already exists, return it
        if os.path.exists(file_path):
            return file_path

        # Fetch from Scryfall API
        time.sleep(0.1)
        url = f"https://api.scryfall.com/cards/named?exact={quote(card_name)}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ Could not fetch data for card '{card_name}' (status {response.status_code})")
            return None

        data = response.json()
        image_url = data.get("image_uris", {}).get("normal")

        if not image_url:
            print(f"⚠️ No image URI found for '{card_name}'")
            return None

        # Download the image
        img_res = requests.get(image_url)
        if img_res.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(img_res.content)
            print(f"✅ Saved image for '{card_name}' → {file_path}")
            return file_path
        else:
            print(f"⚠️ Failed to download image for '{card_name}'")
            return None

    def accessible_colours(self, game, exclude=None):
        if exclude == None:
            l = self.lands_list()
        else:
            l = [item for item in self.lands_list() if item != exclude]
        dict = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "C": 0}
        for land in l:
            for c in land.live_prod(game):
                dict[c] += 1
        return dict

    def necessary_colours(self, allow_duplicates=True):
        l = self.spells_list()
        dict = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0}
        for spell in l:
            for key in dict:
                dict[key] += spell.pips[key]
        return dict

    def contains_searchland(self):
        for card in self.card_list:
            if isinstance(card, SearchLand):
                return True
        return False

    def determine_basics_from_dict(self, input:dict[str, int]) -> str:
        names = []
        for letter in input:
            for _ in range(input[letter]):
                names.append(landtype_map[letter])
        return '\n'.join(names)

#check for filter lands
    def filterlands_present(self):
        for card in self.card_list:
            if isinstance(card, FilterLand):
                return True
        return False









    def permitted_lands(self) -> list:
        #return self._permitted_lands
        return [c for c in self.card_list if c.permitted]

    def reset_card_score(self):
        for card in self.card_list:
            if isinstance(card, Land):
                card.reset_grade()

    def scrap_all_cards(self):
        self.card_list = []













