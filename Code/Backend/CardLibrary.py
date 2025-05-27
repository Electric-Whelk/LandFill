import scrython

#prices': {'usd': '0.07', 'usd_foil': '0.64', 'usd_etched':
result = scrython.cards.Search(q='sidisi')
print(str(result.total_cards()) + " cards:")
for card in result.data():
    print("card: " + card['name'])
    print("cmc: " + card['mana_cost'])
    print("price: " + card['prices']['usd'])
    print("object: " + str(card))