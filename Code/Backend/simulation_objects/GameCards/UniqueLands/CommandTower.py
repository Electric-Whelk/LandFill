from .UniqueLand import UniqueLand
from ... import CardCollections


class CommandTower(UniqueLand):

    def live_prod(self, deck:CardCollections.Deck) -> list[str]:
        return deck.color_id