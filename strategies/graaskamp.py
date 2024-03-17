"""
James Graaskamp's Strategy

> "This rule plays tit for tat for 50 moves, defects on move 51, and then
> plays 5 more moves of tit for tat. A check is then made to see if the player
> seems to be RANDOM, in which case it defects from then on. A check is also
> made to see if the other is TIT FOR TAT, ANALOGY (a program from the
> preliminary tournament), and its own twin, in which case it plays tit for
> tat. Otherwise it randomly defects every 5 to 15 moves, hoping that enough
> trust has been built up so that the other player will not notice these
> defections.
"""

import random
import scipy.stats
import typing

import strategy


class Graaskamp(strategy.Strategy):
    """Graaskamp Implementation"""

    def __init__(self):
        self._state: typing.List[typing.Dict[str, typing.Any]] = dict()

        super().__init__()

    def cooperate(self, pairing) -> bool:
        opponent_name = pairing.opponent_name(me=self)
        opponent_history = pairing.opponent_history(me=self)
        strategy_history = pairing.my_history(me=self)

        if pairing.rounds() == 0:
            self._state[opponent_name] = {
                "last_defection": 0,
                "random_opponent": False,
            }

        if pairing.rounds() < 50:
            return opponent_history[-1] if len(opponent_history) > 0 else True

        if pairing.rounds() == 50:
            return False
        
        if pairing.rounds() <= 55:
            return opponent_history[-1]

        if all(
            opponent_history[i] == strategy_history[i - 1]
            for i in range(1, len(strategy_history))
        ) or all(
            opponent_history[i] == strategy_history[i]
            for i in range(min(len(strategy_history), len(opponent_history)))
        ):
            return True

        state = self._state[opponent_name]

        if state["random_opponent"] == False:
            cooperations = sum([1 for cooperated in opponent_history[-10:] if cooperated])
            defections = sum([1 for cooperated in opponent_history[-10:] if not cooperated])
            p_value = scipy.stats.chisquare([cooperations, defections]).pvalue
            state["random_opponent"] = p_value > 0.05
            # state["random_opponent"] = abs(cooperations - defections) < 5

        if state["random_opponent"]:
            return False

        if random.randint(5, 15) + state["last_defection"] < len(strategy_history):
            state["last_defection"] = len(strategy_history) + 1
            return False

        return opponent_history[-1]
