import scrython
import time

def format_print(item, spacing=""):
    for category in item:
        value = item.get(category)
        if isinstance(value, list):
            for subcategory in value:
                if isinstance(subcategory, dict):
                    format_print(subcategory, spacing=spacing + "  ")
        else:
            print(spacing + category)
            print(spacing + str(value))
            print("")



target = "Wizards of the Coast Customer Service"
time.sleep(0.1)
item = scrython.cards.Search(q=target).data()[0]
format_print(item)

