"""
Base Strategy

Override cooperate().
"""

import random


class Strategy:
    """Strategy Implementation and Interface"""

    def __init__(self):
        """Configures a random name"""
        self._name = f"{self.__class__.__name__}{random.randint(0,9999)}"

    def name(self):
        """Returns the player's name"""
        return self._name

    def cooperate(self, history) -> bool:
        """Implement this in your strategy"""
        raise NotImplementedError()

    def clone(self):
        """Creates another player using the same Strategy"""
        return self.__class__()
