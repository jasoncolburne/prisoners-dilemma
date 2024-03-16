"""
James W. Freidman's Strategy

This strategy defects if its opponent defects even once. It holds grudges.
"""

import strategy


class Friedman(strategy.Strategy):
    """Friedman implementation"""

    def cooperate(self, pairing) -> bool:
        if not all(pairing.opponent_history(me=self)):
            return False

        return True
