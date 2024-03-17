"""
Leslie Downing's Strategy

The original version came from:
https://github.com/Axelrod-Python/Axelrod/blob/v4.13.0/axelrod/strategies/axelrod_first.py#L75-L229

The revised version came from:
https://github.com/Axelrod-Python/TourExec/blob/master/src/strategies/K59R.f
"""

import strategy


class Downing(strategy.Strategy):
    """Downing Implementation"""

    def cooperate(self, pairing) -> bool:
        (opponent_name, opponent_history, strategy_history) = (
            pairing.name_and_histories(me=self)
        )

        if pairing.rounds() == 0:
            coop = 1.0 if len(opponent_history) > 0 else 0.0
            self._state[opponent_name] = {
                "cooperations_after_cooperation": coop,
                "cooperations_after_defection": 0.0,
            }

            return False

        if pairing.rounds() == 1:
            if opponent_history[-1] is True:
                self._state[opponent_name]["cooperations_after_defection"] += 1

            return False

        if opponent_history[-1] is True:
            if strategy_history[-1] is True:
                self._state[opponent_name]["cooperations_after_cooperation"] += 1
            else:
                self._state[opponent_name]["cooperations_after_defection"] += 1

        strategy_cooperations = sum(1 for cooperated in strategy_history if cooperated)
        alpha = (
            self._state[opponent_name]["cooperations_after_cooperation"]
            / (strategy_cooperations)
            if strategy_cooperations != 0
            else 0.37
        )

        strategy_defections = len(strategy_history) - strategy_cooperations
        beta = (
            self._state[opponent_name]["cooperations_after_defection"]
            / strategy_defections
        )

        expected_value_of_cooperating = alpha * 3.0  # 1.5
        expected_value_of_defecting = beta * 5.0 + (1 - beta)  # 2.5 - 0.5 = 2

        if expected_value_of_cooperating > expected_value_of_defecting:
            return True
        if expected_value_of_cooperating < expected_value_of_defecting:
            return False

        return not strategy_history[-1]


class RevisedDowning(strategy.Strategy):
    """Revised Downing Implementation"""

    def cooperate(self, pairing) -> bool:
        (opponent_name, opponent_history, strategy_history) = (
            pairing.name_and_histories(me=self)
        )

        # _pairing.rounds() is updated after both players play, but we must check
        # opponent data even in the middle of the first round
        rounds_played = pairing.rounds()

        if rounds_played == 0:
            self._state[opponent_name] = {
                "nice1": 0,
                "nice2": 0,
            }

            return True

        state = self._state[opponent_name]

        if rounds_played == 0:
            return False

        if rounds_played == 1:
            if opponent_history[-1]:
                state["nice2"] += 1
            return False

        if opponent_history[-1]:
            if strategy_history[-2]:
                state["nice1"] += 1
            else:
                state["nice2"] += 1

        total_cooperations = sum(1 for cooperated in strategy_history if cooperated)
        total_defections = len(strategy_history) - total_cooperations

        good = (
            float(state["nice1"]) / total_cooperations
            if total_cooperations > 0
            else 1.0
        )
        bad = float(state["nice2"]) / total_defections if total_defections > 0 else 0.0

        cooperate = 6.0 * good - 8.0 * bad - 2.0
        defect = 4.0 * good - 5.0 * bad - 1.0

        if cooperate > defect:
            return True

        if defect > cooperate:
            return False

        return not strategy_history[-1]
