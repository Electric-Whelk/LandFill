from simulation_objects.GameCards.PermaUntapped import PermaUntapped
from simulation_objects.Misc.ColorPie import landtype_map


class Verge(PermaUntapped):
    def __init__(self, card, mandatory=False, **kwargs):
        PermaUntapped.__init__(self, card, mandatory=mandatory, **kwargs)
        divided_colours = self.determine_color_primacy(self._produced, card.faces[0].text)
        self._primary = divided_colours["primary"]
        self._secondary = divided_colours["secondary"]
        self._needed_types = [landtype_map[x] for x in self._produced]

    @property
    def primary(self):
        return self._primary

    @property
    def secondary(self):
        return self._secondary

    @property
    def needed_types(self):
        return self._needed_types


    def determine_color_primacy(self, prod, text):
        lines = text.split("\n")
        topline = lines[0]

        primary = self.parse_simple_tapline(topline)

        secondary = "X"
        for color in prod:
            if color != primary:
                secondary = color
        return {
            "primary": primary,
            "secondary": secondary
        }

    def live_prod(self, game):
        active = False
        for needed in self.needed_types:
            if needed in game.battlefield.landtypes_list():
                active = True
                break
        if not active:
            return [self.primary]
        else:
            return [self.primary, self.secondary]

