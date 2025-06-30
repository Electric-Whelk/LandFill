from database_management.models.Card import Card
from Extensions import db
from simulation_objects.GameCard import GameCard
from simulation_objects.Land import Land
from simulation_objects.Spell import Spell

class CardCollection:



    def parse_GameCards(self, card:Card, zone):
        if Card.overall_land:
            return Land(card, zone)
        else:
            return Spell(card, zone)

