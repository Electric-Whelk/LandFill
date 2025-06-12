from database_management.models.Game import Game
from database_management.models.Format import Format
from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face


all_games = {
    Game(_display_name='Paper', _scryfall_name='paper'),
    Game(_display_name='Arena', _scryfall_name='arena'),
    Game(_display_name='MTG Online', _scryfall_name='mtgo')
}

