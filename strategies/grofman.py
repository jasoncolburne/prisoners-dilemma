"""
Bernard Grofman's Strategy

> "If the players did different things on the previous move, this rule
> cooperates with probability 2/7. Otherwise this rule always cooperates."
"""

import random

import strategy


class Grofman(strategy.Strategy):
    """Grofman Implementation"""

    def cooperate(self, pairing) -> bool:
        if (
            pairing.rounds() == 0
            or pairing.opponent_history(me=self)[-1] == pairing.my_history(me=self)[-1]
        ):
            return True

        return 2.0 / 7 > random.random()
