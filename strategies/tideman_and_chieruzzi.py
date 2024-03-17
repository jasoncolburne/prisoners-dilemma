"""
Nicholas Tideman and Paula Chieruzzi's Strategy

> "This rule begins with cooperation and tit for tat. However, when the
> other player finishes his second run of defec- tions, an extra punishment is
> instituted, and the number of punishing defections is increased by one with
> each run of the other's defections. The other player is given a fresh start
> if he is 10 or more points behind, if he has not just started a run of
> defections, if it has been at least 20 moves since a fresh start, if there
> are at least 10 moves remaining, and if the number of defections differs
> from a 50-50 random generator by at least 3.0 standard deviations. A fresh
> start involves two cooperations and then play as if the game had just
> started. The program defects automatically on the last two moves."
"""

import strategy


class TidemanAndChieruzzi(strategy.Strategy):
    """TidemanAndChieruzzi Implementation"""

    def _compute_fresh_start(self, pairing):
        opponent_name = pairing.opponent_name(me=self)
        state = self._state[opponent_name]

        if state["fresh_start"] > 0:
            return

        if pairing.opponent_advantage(me=self) > -10:
            return

        opponent_history = pairing.opponent_history(me=self)

        if not opponent_history[-1] and opponent_history[-2]:
            return

        if pairing.rounds() - state["last_fresh_start_rounds"] < 20:
            return

        if pairing.rounds() > 190:
            return

        cooperations = sum(1 for cooperated in opponent_history if cooperated)
        defections = sum(1 for cooperated in opponent_history if not cooperated)

        n = cooperations + defections
        # std_dev = sqrt(N*p*(1-p)) where p is 1 / 2.
        std_deviation = (n ** (1 / 2)) / 2
        lower = n / 2 - 3 * std_deviation
        upper = n / 2 + 3 * std_deviation
        if (
            state["opponent_defections"] <= lower
            or state["opponent_defections"] >= upper
        ):
            # Opponent deserves a fresh start
            state["retaliations"] = 0
            state["retaliation_length"] = 0
            state["opponent_defections"] = 0
            state["fresh_start"] = 1
            state["last_fresh_start_rounds"] = pairing.rounds()

    def cooperate(self, pairing) -> bool:
        opponent_name = pairing.opponent_name(me=self)
        opponent_history = pairing.opponent_history(me=self)

        if pairing.rounds() == 0:
            self._state[opponent_name] = {
                "retaliations": 0,
                "retaliation_length": 0,
                "opponent_defections": 0,
                "fresh_start": 0,
                "last_fresh_start_rounds": 0,
            }

        state = self._state[opponent_name]

        if pairing.rounds() >= 198:
            return False

        if len(opponent_history) > 0 and opponent_history[-1] is False:
            state["opponent_defections"] += 1

        self._compute_fresh_start(pairing)

        if state["fresh_start"] > 0:
            state["fresh_start"] -= 1
            return True

        if state["retaliations"] > 0:
            state["retaliations"] -= 1
            return False

        if len(opponent_history) > 0 and opponent_history[-1] is False:
            state["retaliation_length"] += 1
            state["retaliations"] = state["retaliation_length"]
            state["retaliations"] -= 1
            return False

        return True
