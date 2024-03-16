"""
Johann Joss' Strategy

This strategy cooperates every turn.
"""

import random

import strategy


class Joss(strategy.Strategy):
    """Joss Implementation"""

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if len(opponent_history) > 0 and not opponent_history[-1]:
            return False

        if random.random() >= 0.9:
            return False

        return True
