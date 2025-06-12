from database_management.models.Game import Game
from database_management.models.Format import Format
from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face


all_formats = {
    Format(_display_name='Standard', _scryfall_name='standard',
           _copies = 4, _deck_size = 60,
           _hard_max = False, _arena = True,
           _mtg_online = True, _paper=True),
    Format(_display_name='Modern', _scryfall_name='modern',
           _copies = 4, _deck_size=60,
           _hard_max=False, _arena=False,
           _mtg_online=True, _paper=True),
    Format(_display_name='Legacy', _scryfall_name='legacy',
           _copies=4, _deck_size=60,
           _hard_max=False, _arena=False,
           _mtg_online=True, _paper=True),
    Format(_display_name='EDH', _scryfall_name='commander',
           _copies=1, _deck_size=100,
           _hard_max=True, _arena=False,
           _mtg_online=False, _paper=True),
    Format(_display_name='Limited', _scryfall_name='NA',
           _copies=4, _deck_size=40,
           _hard_max=False, _arena=True,
           _mtg_online=True, _paper=True)
}