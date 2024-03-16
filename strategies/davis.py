"""
Morton Davis' Strategy

> "A player starts by cooperating for 10 rounds then plays Grudger,
> defecting if at any point the opponent has defected."
"""

import strategy


class Davis(strategy.Strategy):
    """Davis Implementation"""

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if len(opponent_history) < 10:
            return True

        if any(cooperated == False for cooperated in opponent_history[10:]):
            return False

        return True
