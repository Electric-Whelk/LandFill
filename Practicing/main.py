import scrython



def decorator(func):
    def wrapper(self):
        top = "wrapping...\n"
        mid = func(self)
        bottom = "\nwrapped!"
        return top + mid[0] + bottom
    return wrapper

class Musician:
    def __init__(self, name , genre, magnumOpus):
        self._name = name
        self._genre = genre
        self._magnumOpus = magnumOpus

    def __str__(self):
        return self.name

    @property
    def name(self):
        print("getting name..!")
        return self._name

    def getMembers(self):
        return self.name

class Band(Musician):
    def __init__(self, name, genre, magnumOpus, members):
        super().__init__(name, genre, magnumOpus)
        self.members = members


    def __iter__(self):
        self.pos = 0
        return self

    def __next__(self):
        length = len(self.members)
        try:
            output = self.members[self.pos]
            self.pos += 1
            return output
        except:
            raise StopIteration

    @decorator
    def getMembers(self):
        return self.members


playlist = [
    Musician("Joanna Newsom", "Indie Folk", "Divers"),
    Band("Fugazi", "Post-Hardcore", "Red Medicine", ["Ian MacKaye", "Guy Picciotto", "Joe Lally", "Brendan Canty"])
       ]

#set = Set.find('dsk')
print(playlist[1].name)

#prices': {'usd': '0.07', 'usd_foil': '0.64', 'usd_etched':
result = scrython.cards.Search(q='sidisi')
print(str(result.total_cards()) + " cards:")
for card in result.data():
    print("card: " + card['name'])
    print("cmc: " + card['mana_cost'])
    print("price: " + card['prices']['usd'])
    print("object: " + str(card))

"""'Black Lotus'
>> > card.id()
'bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd'
>> > card.oracle_text()
'{T}, Sacrifice Black Lotus: Add three mana of any one color to your mana pool.'"""