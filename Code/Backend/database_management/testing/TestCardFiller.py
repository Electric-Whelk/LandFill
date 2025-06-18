import scrython
import time

count = 1

with open("database_management/fillscripts/TestCards.py", "w") as test_cards:
    test_cards.seek(0)
    test_cards.truncate()
    test_cards.write("test_cards = [")

def format_test_data(term, description):
    time.sleep(0.1)
    global count
    data = scrython.cards.Search(q=term).data()
    for item in data:
        comment = "#" + str(count) + ": " + item["name"] + " - " + description
        with open("database_management/fillscripts/TestCards.py", "a") as test_cards:
            test_cards.write("\n")
            test_cards.write(comment)
            test_cards.write("\n")
            test_cards.write(str(item) + ",")
        print("Added " + item["name"] + "...")
    count += 1


format_test_data("Mikaeus the Unhallowed", "purespell")
format_test_data("Tasigur, the Golden Fang", "not a shock land")
format_test_data("Blood Crypt", "shock land")
format_test_data("Steam Vents", "another shock land")
format_test_data("Kozilek, the Great Distortion", "colorlessmana")
format_test_data("Scalding Tarn", "pureland")
format_test_data("Riverglide Pathway", "landland")
format_test_data("Bala Ged Recovery", "landspell which can be played as land or spell")
format_test_data("Westvale Abbey", "landspell which can be land but not spell")
format_test_data("Aclazotz, Deepest Betrayal", "landspell which can be spell but not land")
format_test_data("Plargg, Dean of Chaos // Augusta, Dean of Order", "spellspell")
format_test_data("Ulrich of the Krallenhorde", "werewolf")
format_test_data("Sasaya, Orochi Ascendant", "flip")
format_test_data("Turn // Burn", "split")
format_test_data("Destined // Lead", "aftermath")
format_test_data("Murmuring Bosk", "not_in_cycle")
format_test_data("reflecting pool", "conditional_colors")
format_test_data("llanowar elves", "mana_dork")
format_test_data("Azorius Chancery", "multiproduce")
format_test_data("Nykthos, Shrine to Nyx", "conditional_multiproduce")
format_test_data("Blue Sun's Zenith", "x_in_mana_cost")
format_test_data("Asmoranomardicadaistinaculdacar", "no cost, no land")
format_test_data("Bone Saw", "cost zero, no land")
format_test_data("Clifftop Retreat", "check land 1")
format_test_data("Sulfur Falls", "check land 2")
format_test_data("Necroblossom Snarl", "reveal land 1")
format_test_data("Fortified Village", "reveal land 2")
format_test_data("Fire-Lit Thicket", "filter land 1")
format_test_data("Twilight Mire", "filter land 2")
format_test_data("Morphic Pool", "bond land 1")
format_test_data("Vault of Champions", "bond land 2")
format_test_data("Tropical Island", "OG Dual 1")
format_test_data("Taiga", "OG Dual 2")
format_test_data("Blazemire Verge", "Verge dual 1")
format_test_data("Riverpyre Verge", "Verge dual 2")
format_test_data("Silent Clearing", "PainDraw 1")
format_test_data("Waterlogged Grove", "PainDraw 2")
format_test_data("Lovestruck Beast", "Adventure" )
format_test_data("Betor, Kin to All", "standard legal")
format_test_data("Chalice of the Void", "restricted in vintage")

format_test_data("little girl", "manually adding")
format_test_data("B.F.M. (Big Furry Monster)", "unset duplication nonsense")
format_test_data("Scavenger Hunt", "even more unset duplication nonsense")



with open("database_management/fillscripts/TestCards.py", "a") as test_cards:
    test_cards.write("]")
