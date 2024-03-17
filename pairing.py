"""
A cooperation history between two strategies.
"""

import typing

import strategy


class Pairing:
    """History Immplementation"""

    def __init__(
        self, player_one: strategy.Strategy, player_two: strategy.Strategy
    ) -> None:
        self._players: typing.List[strategy.Strategy] = [player_one, player_two]

        self._history: typing.Dict[str, typing.List[bool]] = {
            player_one.name(): [],
            player_two.name(): [],
        }

        self._score: typing.Dict[str, int] = {
            player_one.name(): 0,
            player_two.name(): 0,
        }

    def players(self) -> typing.List[strategy.Strategy]:
        """Returns players"""
        return self._players

    def name_and_histories(
        self, me: strategy.Strategy
    ) -> typing.Tuple[str, typing.List[bool], typing.List[bool]]:
        """Returns relevant pairing details"""
        return (self.opponent_name(me), self.opponent_history(me), self.my_history(me))

    def my_history(self, me: strategy.Strategy) -> typing.List[bool]:
        """Returns the history of the player"""
        return self._history[me.name()]

    def opponent_history(self, me: strategy.Strategy) -> typing.List[bool]:
        """Returns the history of the opponent"""
        return self._history[self.opponent_name(me=me)]

    def opponent_name(self, me: strategy.Strategy) -> str:
        """Returns the opponent name"""
        return [player.name() for player in self._players if player != me][0]

    def create(self, rounds: int) -> None:
        """Simulates a number of rounds of play"""
        while rounds > 0:
            p1 = self._players[0]
            one = p1.cooperate(self)
            self._history[p1.name()].append(one)

            p2 = self._players[1]
            two = p2.cooperate(self)
            self._history[p2.name()].append(two)

            if one and two:
                self._score[p1.name()] += 3
                self._score[p2.name()] += 3
            elif one:
                self._score[p2.name()] += 5
            elif two:
                self._score[p1.name()] += 5
            else:
                self._score[p1.name()] += 1
                self._score[p2.name()] += 1

            rounds -= 1

    def rounds(self) -> int:
        """Returns the number of rounds played"""
        return len(self._history[self._players[1].name()])

    def __str__(self) -> str:
        p1 = self._players[0].name()
        p1_pretty = self._players[0].pretty_name()
        p2 = self._players[1].name()
        p2_pretty = self._players[1].pretty_name()
        return f"{p1_pretty}: {self._score[p1]}, {p2_pretty}: {self._score[p2]}"

    def debug(self) -> None:
        """Prints debug information to stdout"""
        p1 = self._players[0].name()
        p2 = self._players[1].name()

        print(
            f"{' ' * max(len(p2) - len(p1), 0) + p1}: "
            + f"{''.join('✓' if b else '✗' for b in self._history[p1])}"
        )
        print(
            f"{' ' * max(len(p1) - len(p2), 0) + p2}: "
            + f"{''.join('✓' if b else '✗' for b in self._history[p2])}"
        )

    def score(self, player: strategy.Strategy, first_only=False) -> int | None:
        """Obtains the current score for a player"""
        if first_only:
            if player == self._players[0]:
                return self._score[player.name()]
        else:
            if player.name() in self._score:
                return self._score[player.name()]

        return None

    def opponent_advantage(self, me: strategy.Strategy) -> int:
        """Returns the oppoennt advantage"""
        return self.score(
            player=[player for player in self._players if player != me][0]
        ) - self.score(player=me)
