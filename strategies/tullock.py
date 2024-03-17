"""
Gordon Tullock's Strategy

> "This rule cooperates on the first eleven moves. It then cooperates 10%
> less than the other player has cooperated on the preceding ten moves. This
> rule is based on an idea developed in Overcast and Tullock (1971). Professor
> Tullock was invited to specify how the idea could be implemented, and he did
> so out of scientific interest rather than an expectation that it would be a
> likely winner."
"""

import random

import strategy


class Tullock(strategy.Strategy):
    """Tullock Implementation"""

    def cooperate(self, pairing) -> bool:
        if pairing.rounds() < 11:
            return True

        opponent_history = pairing.opponent_history(me=self)

        cooperation_count = sum(
            1 for cooperated in opponent_history[-10:] if cooperated
        )
        probability_to_cooperate = cooperation_count / 10.0

        return max(0.0, probability_to_cooperate - 0.10) > random.random()
