"""
Martin Shubik's Strategy

> "I will play my move 1 to begin with and will continue to do so, so long
> as my information shows that the other player has chosen his move 1. If my
> information tells me he has used move 2, then I will use move 2 for the
> immediate k subsequent periods, after which I will resume using move 1. If
> he uses his move 2 again after I have resumed using move 1, then I will
> switch to move 2 for the k + 1 immediately subsequent periods . . . and so
> on, increasing my retaliation by an extra period for each departure from the
> (1, 1) steady state."
"""

import strategy


class Shubik(strategy.Strategy):
    """Shubik Implementation"""

    def cooperate(self, pairing) -> bool:
        (opponent_name, opponent_history, strategy_history) = (
            pairing.name_and_histories(me=self)
        )

        if pairing.rounds() == 0:
            self._state[opponent_name] = {
                "retaliations": 0,
                "retaliation_length": 0,
            }

            return True

        state = self._state[opponent_name]
        if (
            not opponent_history[-1]
            and strategy_history[-1]
            and state["retaliations"] == 0
        ):
            state["retaliation_length"] += 1
            state["retaliations"] = state["retaliation_length"]

        if state["retaliations"] > 0:
            state["retaliations"] -= 1
            return False

        return True
