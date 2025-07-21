
from ..Land import Land

class UntappableLand(Land):

    def run_etb(self, game):
        if not self.enters_untapped(game):
            #print(f"{self} entering tapped...")
            pass