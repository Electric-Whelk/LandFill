import random

def generate(x):
    diceRoll = random.randrange(0, x)
    strMax = str(x)
    strDice = str(diceRoll)
    print("Alright, here's a number between 0 and " + strMax + ":\n" + strDice)

generate(10)