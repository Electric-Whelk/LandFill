
class WodgeSocket:
    def __init__(self, wodge, castable, uncastable):
        self._wodge = wodge
        self._castable = castable
        self._uncastable = uncastable
        self._overall_castable = len(self._castable) > 0


