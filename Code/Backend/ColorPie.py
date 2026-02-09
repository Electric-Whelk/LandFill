
class ColorPie():
    def __init__(self, value = 1):
        self._value = value
        self._colors =  [
            "W",
            "U",
            "B",
            "R",
            "G"
        ]

        self._lands = [
            "Plains",
            "Island",
            "Swamp",
            "Mountain",
            "Forest"
        ]

        self._color_score = {
        "W": 2,
        "U": 3,
        "B": 5,
        "R": 7,
        "G": 11
        }

        self._land_score = {
        "Plains": 2,
        "Island": 3,
        "Swamp": 5,
        "Mountain": 7,
        "Forest": 11
        }

    #getters and setters
    @property
    def value(self) -> int:
        return self._value
    @value.setter
    def value(self, value: int):
        self._value = value

    @property
    def count(self) -> int:
        output = 0
        for color in self.colors:
            prime = self.score[color]
            if self.modzero(self.value, prime):
                output += 1
        return output

    @property
    def colors(self):
        return self._colors

    @property
    def lands(self):
        return self._lands

    @property
    def score(self) ->dict:
        return self._color_score

    @property
    def l_score(self):
        return self._land_score

    #parsing functions
    def prime_mult(self, prime):
        if not self.modzero(self.value, prime):
            self.value *= prime

    def produces_needed(self, produces_score: int) -> bool:
        return self.modzero(self.value, produces_score)

    def parse_colors(self, color_list:list[str]):
        for color in self.colors:
            if color in color_list:
                self.prime_mult(self.score[color])

    def parse_lands(self, land_list:list[str]):
        for land in self.lands:
            if land in land_list:
                self.prime_mult(self.l_score[land])






    #internally useful functions
    def modzero(self, x:int, y:int) -> bool:
        try:
            return x % y == 0
        except ZeroDivisionError:
            return False



