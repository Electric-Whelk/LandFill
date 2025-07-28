from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face
from Extensions import db
from random import shuffle

from simulation_objects.GameCards import CommandTower, BondLand, DualLand, BattleLand, FastLand, SlowLand, PainLand, \
    HorizonLand
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.MiscLand import MiscLand
from simulation_objects.GameCards.SearchLands import SearchLand
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.RampLands.FilterLand import FilterLand
from simulation_objects.GameCards.TappedCycles.GuildGate import GuildGate
from simulation_objects.GameCards.TappedCycles.TriTap import TriTap
from simulation_objects.GameCards.UntappableCycles.RevealLand import RevealLand
from simulation_objects.GameCards.RampLands.BounceLand import BounceLand
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.GameCards.TappedCycles.Triome import Triome
from simulation_objects.GameCards.UntappableCycles.CheckLand import CheckLand
from simulation_objects.GameCards.UntappableCycles.ShockLand import ShockLand
from simulation_objects.Misc.ColorPie import landtype_map


class CardCollection:
    def __init__(self):
        self._cards = []

    #getters and setters
    @property
    def card_list(self) -> list[GameCard]:
        return self._cards
    @card_list.setter
    def card_list(self, cards: list[GameCard]):
        self._cards = cards

    def length(self):
        return len(self.card_list)

    #sublists
    def lands_list(self) -> list[Land]:
        return [x for x in self.card_list if isinstance(x, Land)]

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
        #print(f"looking up card {name}...")
        face = db.session.query(Face).filter(Face._name == name).first()
        card = db.session.query(Card).filter(Card._id == face.card_id).first()
        return card

    def parse_cards_from_json(self, cards):
        as_list = cards.split("\n")
        output = []
        for name in as_list:
            #print(f"Parsing {name}")
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
                #case "Filter Lands":
                    #return FilterLand(card, mandatory)
                case "Check Lands":
                    return CheckLand(card, mandatory)
                case "Reveal Lands":
                    return RevealLand(card, mandatory)
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
        match card.name:
            case "Command Tower":
                return CommandTower(card, mandatory)
            case _:
                return MiscLand(card, mandatory)

    def print_all(self):
        for card in self.card_list:
            print(f"{card.name}")



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










