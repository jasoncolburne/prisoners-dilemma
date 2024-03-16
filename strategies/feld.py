"""
Scott Feld's Strategy

> "This rule starts with tit for tat and gradually lowers its probability of
> cooperation following the other's cooperation to .5 by the two hundredth
> move. It always defects after a defection by the other."
"""

import random

import strategy


class Feld(strategy.Strategy):
    """Feld Implementation"""

    def probability_of_cooperation(self, rounds):
        if rounds > 200:
            return 0.5

        return 0.5 * (200.0 - rounds) / 200 + 0.5

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if not opponent_history:
            return True

        if not opponent_history[-1]:
            return False

        p = self.probability_of_cooperation(pairing.rounds())

        if p > random.random():
            return True

        return False
