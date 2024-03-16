"""
Tit for two Tats Strategy

This strategy cooperates unless the its opponent defected in both of the most recent
two rounds.
"""

import strategy


class TitForTwoTats(strategy.Strategy):
    """TitForTwoTats Implementation"""

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if len(opponent_history) < 2:
            return True

        if not any(opponent_history[-2:]):
            return False

        return True
