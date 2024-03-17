"""
William Stein and Amnon Rapoport's Strategy

> "This rule plays tit for tat except that it cooperates on the first four
> moves, it defects on the last two moves, and every fifteen moves it checks
> to see if the opponent seems to be playing randomly. This check uses a
> chi-squared test of the other's transition probabilities and also checks for
> alternating moves of CD and DC.
"""

import scipy.stats
import typing

import strategy


class SteinAndRapoport(strategy.Strategy):
    """SteinAndRapoport Implementation"""

    def __init__(self):
        self._state: typing.List[typing.Dict[str, typing.Any]] = dict()

        super().__init__()

    def cooperate(self, pairing) -> bool:
        opponent_name = pairing.opponent_name(me=self)
        opponent_history = pairing.opponent_history(me=self)
        strategy_history = pairing.my_history(me=self)

        cooperations = sum([1 for cooperated in opponent_history if cooperated])
        defections = len(opponent_history) - cooperations

        rounds = pairing.rounds()

        if rounds == 0:
            self._state[opponent_name] = {
                "random_opponent": False,
                "misplays": 0,
            }

        if rounds < 4:
            return True

        if rounds < 14:
            return opponent_history[-1]

        if rounds >= 198:
            return False

        state = self._state[opponent_name]

        if state["random_opponent"]:
            return False

        if strategy_history[-2] != opponent_history[-1]:
            state["misplays"] += 1

        if (rounds + 1) % 15 == 0:
            state["random_opponent"] = (
                scipy.stats.chisquare([cooperations, defections]).pvalue > 0.05 or
                state["misplays"] > 3
            )

        return opponent_history[-1]
