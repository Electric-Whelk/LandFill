from simulation_objects.CardCollectiions.CardCollection import CardCollection

class Battlefield(CardCollection):


    #game actions
    def untap(self):
        for card in self._cards:
            card.tapped = False

    #game information
    def determine_available_mana(self):
        pass



