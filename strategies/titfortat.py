"""
Tit for Tat Strategy

This strategy repeats its opponents last move. Also known as eye for an eye, or
reciprical.
"""

import strategy


class TitForTat(strategy.Strategy):
    """TitForTat Implementation"""

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if len(opponent_history) == 0:
            return True

        return opponent_history[-1]
