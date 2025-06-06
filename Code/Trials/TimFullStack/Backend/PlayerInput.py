from Scrythonning.CardLibrary import CardLibrary

class PlayerInput:
    def __init__(self, non_lands, format, quantity):
        #factors that are determined once at the start and are not changed as the program iterates
        self._db = CardLibrary()
        self._input_cards = self.parse_input_cards(non_lands)
        self._non_lands = self.extract_by_card_type(self._input_cards, "land")
        self._format = format
        self._quantity = quantity
        self._colors = self.determine_colors()

    #calculating functions used in the input, listed in order called
    def parse_input_cards(self, input):
        card_names = self.tokenize_input_cards(input)
        cards = self.get_cards_from_list(card_names)
        return cards

    def tokenize_input_cards(self, input):
        return input.split("\n")

    def determine_colors(self):
        return 0

    #setter and getter functions
    @property
    def input_cards(self):
        return self._input_cards

    @input_cards.setter
    def input_cards(self, value):
        self._input_cards = value

    #generally useful functions (alphabetized)

    def extract_by_card_type(self, cards, func):
        for card in cards:
            print(card.types)


    def get_cards_from_list(self, input):
        output = []
        for name in input:
            new = self._db.lookup_by_name(name)
            output.append(new)

        return output
