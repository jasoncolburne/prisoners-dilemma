"""
Freidman Strategy

This strategy defects if its opponent defects even once. It holds grudges.
"""

import strategy


class Friedman(strategy.Strategy):
    """Friedman implementation"""

    def cooperate(self, history) -> bool:
        if not all(history.opponent(me=self)):
            return False

        return True
