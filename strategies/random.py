import random

import strategy


class Random(strategy.Strategy):
    def cooperate(self, _history) -> bool:
        if random.randint(0, 1) == 0:
            return True

        return False
