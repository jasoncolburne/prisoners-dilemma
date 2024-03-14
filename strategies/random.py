"""
Random Strategy

This strategy randomly cooperates 50% of the time.
"""

import random

import strategy


class Random(strategy.Strategy):
    """Random implementation"""

    def cooperate(self, _history) -> bool:
        if random.randint(0, 1) == 0:
            return True

        return False
