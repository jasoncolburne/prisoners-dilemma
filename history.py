"""
A cooperation history between two strategies.
"""

import typing

import strategy


class History:
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

    def mine(self, me: strategy.Strategy) -> typing.List[bool]:
        """Returns the history of the player"""
        return self._history[me.name()]

    def opponent(self, me: strategy.Strategy) -> typing.List[bool]:
        """Returns the history of the opponent"""
        return self._history[
            [player.name() for player in self._players if player != me][0]
        ]

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
        return len(self._history[self._players[0].name()])

    def __str__(self) -> str:
        p1 = self._players[0].name()
        p2 = self._players[1].name()
        return f"{p1}: {self._score[p1]}, {p2}: {self._score[p2]}"

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

    def score(self, player: strategy.Strategy) -> int | None:
        """Obtains the current score for a player"""
        if player.name() in self._score:
            return self._score[player.name()]

        return None
