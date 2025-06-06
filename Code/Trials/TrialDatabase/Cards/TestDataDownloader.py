import scrython
import time

count = 1

def format_test_data(term, description):
    time.sleep(0.1)
    global count
    item = scrython.cards.Search(q=term).data()[0]
    comment = "#" + str(count) + ": " + item["name"] + " - " + description
    print(comment)
    print(str(item) + ",")
    count += 1

format_test_data("Mikaeus the Unhallowed", "purespell")
format_test_data("Kozilek, the Great Distortion", "colorlessmana")
format_test_data("Scalding Tarn", "pureland")
format_test_data("Bala Ged Recovery", "landspell")
format_test_data("Riverglide Pathway", "landland")
format_test_data("Plargg, Dean of Chaos // Augusta, Dean of Order", "spellspell")
format_test_data("Ulrich of the Krallenhorde", "werewolf")
format_test_data("Sasaya, Orochi Ascendant", "flip")
format_test_data("Turn // Burn", "split")
format_test_data("Destined // Lead", "aftermath")
format_test_data("Westvale Abbey", "land_enough")
format_test_data("Murmuring Bosk", "not_in_cycle")
format_test_data("reflecting pool", "conditional_colors")
format_test_data("llanowar elves", "mana_dork")
format_test_data("Azorius Chancery", "multiproduce")
format_test_data("Nykthos, Shrine to Nyx", "conditional_multiproduce")
format_test_data("Blue Sun's Zenith", "x_in_mana_cost")
format_test_data("Asmoranomardicadaistinaculdacar", "no cost, no land")
format_test_data("Bone Saw", "cost zero, no land")


