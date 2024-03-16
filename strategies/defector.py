"""
Defective Strategy

This strategy defects every turn.
"""

import strategy


class Defector(strategy.Strategy):
    """Defector Strategy"""

    def cooperate(self, _pairing) -> bool:
        return False
