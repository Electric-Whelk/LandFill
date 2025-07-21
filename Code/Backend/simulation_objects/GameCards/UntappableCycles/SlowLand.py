from simulation_objects.GameCards.UntappableCycles.UntappableLand import UntappableLand

class SlowLand(UntappableLand):

    def enters_untapped(self, game) -> bool:
        return len([x for x in game.battlefield.lands_list() if x != self]) >= 2

