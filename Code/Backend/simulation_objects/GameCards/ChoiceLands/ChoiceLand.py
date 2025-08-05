from simulation_objects.GameCards import Land


class ChoiceLand(Land):
    def __init__(self, card, mandatory, **kwargs):
        Land.__init__(self, card, mandatory, **kwargs)
        self._generic_price = self._none_price = 1
        self._committed = None
        self._display_name = self._name


    def __repr__(self):
        return self._display_name

    @property
    def display_name(self):
        return self._display_name
    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def committed(self):
        return self._committed
    @committed.setter
    def committed(self, val):
        self._committed = val


    def reset_choices(self):
        self._committed = None
        self._display_name = self._name
        self._generic_price = self._none_price = 1





