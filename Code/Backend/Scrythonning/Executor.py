from CardLibrary import CardLibrary
from Card import Card


lib = CardLibrary()

"""results = lib.lookup_by_type("type:artifact type:creature type:legendary")
for card in results:
    print(card.name)"""

#lib.lookup_by_name("Mikaeus, the Unhallowed").print()
#print("//////////")
checkovgun = "type:land (game:paper) cmc=0 usd<0.1 usd>0"
original = "type:land (game:paper) cmc=0"
results = []

"""
results = lib.lookup_by_type("type:land (game:paper) cmc=0")
i = 1
with open("../land_regexing/typedlandsog.txt", "w") as f:
    for card in results:
        name = card.name
        subtypes = str(card.subtypes)
        text = card.oracle_text.replace("\n", " ")
        f.write(name + " | " + subtypes + " | " + text + "\n")
        print(str(i) + " " + name)
        i+=1
#Hall of Heliod's generosity"""

lib.lookup_by_name("Sheoldred")