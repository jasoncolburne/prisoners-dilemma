"""
Rudy Nydegger's Strategy

> "The program begins with tit for tat for the first three moves, except
> that if it was the only one to cooperate on the first move and the only one
> to defect on the second move, it defects on the third move. After the third
> move, its choice is determined from the 3 preceding outcomes in the
> following manner. Let A be the sum formed by counting the other's defection
> as 2 points and one's own as 1 point, and giving weights of 16, 4, and 1 to
> the preceding three moves in chronological order. The choice can be
> described as defecting only when A equals 1, 6, 7, 17, 22, 23, 26, 29, 30,
> 31, 33, 38, 39, 45, 49, 54, 55, 58, or 61. Thus if all three preceding moves
> are mutual defection, A = 63 and the rule cooperates.  This rule was
> designed for use in laboratory experiments as a stooge which had a memory
> and appeared to be trustworthy, potentially cooperative, but not gullible
> (Nydegger, 1978)."
"""

import strategy


DEFECTIVE = [1, 2, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61]


class Nydegger(strategy.Strategy):
    """Nydegger Implementation"""

    def sum(self, strategy_history, opponent_history, index):
        """Compute the Nydegger sum for a given index"""
        match (strategy_history[index], opponent_history[index]):
            case (True, True):
                return 0
            case (False, True):
                return 1
            case (True, False):
                return 2
            case (False, False):
                return 3

    def compute_a(self, strategy_history, opponent_history):
        """Compute the A value"""
        return (
            self.sum(strategy_history, opponent_history, -1)
            + self.sum(strategy_history, opponent_history, -2) * 4
            + self.sum(strategy_history, opponent_history, -3) * 16
        )

    def cooperate(self, pairing) -> bool:
        strategy_history = pairing.my_history(me=self)
        opponent_history = pairing.opponent_history(me=self)

        rounds = pairing.rounds()

        if rounds in [0, 1]:
            return opponent_history[-1] if len(opponent_history) > 0 else True

        if rounds == 2:
            if opponent_history[-2] is False and opponent_history[-1] is True:
                return False

            return opponent_history[-1]

        a = self.compute_a(strategy_history, opponent_history)
        return a not in DEFECTIVE
