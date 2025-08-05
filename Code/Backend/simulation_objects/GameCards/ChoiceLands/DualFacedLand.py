from simulation_objects.GameCards.SubLand import SubLand
from simulation_objects.GameCards.ChoiceLands import ChoiceLand


class DualFacedLand(ChoiceLand):
    def __init__(self, card, mandatory, **kwargs):
        ChoiceLand.__init__(self, card, mandatory, **kwargs)
        face_one = self.create_face(card, card.faces[0])
        face_two = self.create_face(card, card.faces[1])
        self._sublands = [face_one, face_two]
        print(f"My name is {self} and I have the following faces:")
        for face in self._sublands:
            print(f"{face.name} -> {face.produced}")

    @property
    def sublands(self):
        return self._sublands

    def create_face(self, card, face):
        name = face.name
        color = [self.parse_simple_tapline(face.text)]
        output = SubLand(card, produced=color, name=name)
        return output


    def live_prod(self, game):
        if self.committed is None:
            #print(f"{self} can tap for {self.produced}")
            return self.produced
        else:
            #print(f"{self.name} can tap for {self.committed}")
            return self.committed


    def tap_for_specific_v2(self, color, game):
        if self.committed is None:
            if color in ["None", "Gen"]:
                choice = game.filter_by_most_produced(self._sublands, library=True)
                self.commit_subland(choice)
            else:
                for subland in self.sublands:
                    #print(f"{subland.name} -> {subland.produced}")
                    if color in subland.produced:
                        self.commit_subland(subland)
                        break
            if self.committed is None:
                raise Exception(f"Dual faced land commit error for {self}")

    def commit_subland(self, subland):
        self.committed = subland.produced
        self.display_name = subland.name
        self._generic_price = self._none_price = 2

    def set_price(self, game, color):
        if color == "None":
            return self.none_price
        if not self.tapped:
            if color == "Gen":
                return self.generic_price
            if color in self.live_prod(game):
                return self.color_price
        return 9999





