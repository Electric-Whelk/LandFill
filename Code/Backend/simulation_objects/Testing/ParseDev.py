import json

from AppFactory import create_app
from simulation_objects.CardCollections import Deck, MonteCarlo
from simulation_objects import InputParser

with open("output_files/deck_submissions/sample_input.json", "r") as json_file:
    data = json.load(json_file)

app = create_app()

simulating = False

with app.app_context():
    player_deck = Deck()
    imp = InputParser()
    monty = MonteCarlo(player_deck)


    decklist = imp.parse_decklist(data.get("deckList"))
    partner = imp.parse_partner(data.get("partner"))
    player_deck.setup(decklist, data.get("commander"), partner=partner, remove_lands=data.get("removeLands"))
    if simulating:
        monty.setup()
        monty.fill_heap()
        monty.set_rankings([])
        monty.run()

    newcats = imp.decklist_to_categories(player_deck.card_list)
    print("----Archidekt----\n")
    print(imp.format_archidekt_lands())
    print("----MoxBox----\n")
    print(imp.format_moxbox_lands())
    print("----TappedOut----\n")
    print(imp.format_tappedout_lands())

