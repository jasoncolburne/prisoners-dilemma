"""
Cooperative Strategy

This strategy cooperates every turn.
"""

import strategy


class Cooperator(strategy.Strategy):
    """Cooperator Implementation"""

    def cooperate(self, _pairing) -> bool:
        return True
