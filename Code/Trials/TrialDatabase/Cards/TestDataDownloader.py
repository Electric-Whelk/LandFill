import scrython

def one_card_search(term, description):
    item = scrython.cards.Search(q=term).data()[0]
    comment = "#" + description
    print(comment)
    print(str(item) + ",")
    #print("\"" + outp['name'] + "\":  " + str(outp) + ",")
    #return outp


one_card_search("Mikaeus the Unhallowed", "purespell")
one_card_search("Kozilek, the Great Distortion", "colorlessmana")
"""
one_card_search("Scalding Tarn", "pureland")
one_card_search("Bala Ged Recovery", "landspell")
one_card_search("Riverglide Pathway", "landland")
one_card_search("Plargg, Dean of Chaos // Augusta, Dean of Order", "spellspell")
one_card_search("Ulrich of the Krallenhorde", "werewolf")
one_card_search("Sasaya, Orochi Ascendant", "flip")
one_card_search("Turn // Burn", "split")
one_card_search("Destined // Lead", "aftermath")
one_card_search("Westvale Abbey", "land_enough")
one_card_search("Murmuring Bosk", "not_in_cycle")
one_card_search("reflecting pool", "conditional_colors")
one_card_search("llanowar elves", "mana_dork")
one_card_search("Azorius Chancery", "multiproduce")
one_card_search("Nykthos, Shrine to Nyx", "conditional_multiproduce")
one_card_search("Blue Sun's Zenith", "x_in_mana_cost")
"""

