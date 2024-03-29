"""
Base Strategy

Override cooperate().
"""

import typing

import random


class Strategy:
    """Strategy Implementation and Interface"""

    def __init__(self):
        """Configures a random name and empty state"""
        self._name: str = f"{self.__class__.__name__}{random.randint(0,9999)}"
        self._state: typing.List[typing.Dict[str, typing.Any]] = {}

    def pretty_name(self):
        """Returns a name without the random identifier"""
        return self._name.strip("0123456789")

    def name(self):
        """Returns the player's name"""
        return self._name

    def cooperate(self, _pairing) -> bool:
        """Implement this in your strategy"""
        raise NotImplementedError()

    def clone(self):
        """Creates another player using the same Strategy"""
        return self.__class__()

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.__str__()
