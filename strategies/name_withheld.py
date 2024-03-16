"""
Name Withheld's Strategy

> "This rule has a probability of cooperating, P, which is initially 30% and
> is updated every 10 moves. P is adjusted if the other player seems random,
> very cooperative, or very uncooperative. P is also adjusted after move 130
> if the rule has a lower score than the other player. Unfortunately, the
> complex process of adjustment frequently left the probability of cooperation
> in the 30% to 70% range, and therefore the rule appeared random to many
> other players."
"""

import random

import strategy


class NameWithheld(strategy.Strategy):
    """NameWithheld Implementation"""

    def cooperate(self, _pairing) -> bool:
        return random.random() * 0.4 + 0.3 > random.random()
