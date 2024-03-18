"""
Main
"""

import math
import random
import sys
import typing

# local
import pairing
import strategy

# strategies
import strategies.cooperator
import strategies.davis
import strategies.defector
import strategies.downing
import strategies.feld
import strategies.friedman
import strategies.graaskamp
import strategies.grofman
import strategies.joss
import strategies.name_withheld
import strategies.nydegger
import strategies.random
import strategies.shubik
import strategies.stein_and_rapoport
import strategies.tideman_and_chieruzzi
import strategies.titfortat
import strategies.titfortwotats
import strategies.tullock

ROUNDS = 200
DEBUG = False
SORTED = True  # set to False to preserve tournament ordering as results may differ
BOTH_DIRECTIONS = (
    False  # set to True to consider results when starting from both positions
)


# pylint: disable=too-many-locals
def simulate(
    _strategies: typing.List[strategy.Strategy],
    rounds: int = ROUNDS,
    debug_strategies: typing.List[str] = None,
) -> None:
    """Simulates the classic prisoner's dilemma tournament"""

    if debug_strategies is None:
        debug_strategies = []

    pairings: typing.List[pairing.Pairing] = []
    for _strategy in _strategies:
        twin = _strategy.clone()
        pairings.append(pairing.Pairing(_strategy, twin))
        if BOTH_DIRECTIONS:
            pairings.append(pairing.Pairing(twin, _strategy))

        others = [
            __strategy
            for __strategy in _strategies
            if _strategy.name() != __strategy.name()
        ]
        for other in others:
            pairings.append(pairing.Pairing(_strategy, other))

    while any(_pairing.rounds() < rounds for _pairing in pairings):
        relevant = [_pairing for _pairing in pairings if _pairing.rounds() < rounds]
        random.shuffle(relevant)
        relevant[0].create(1)

    for _pairing in pairings:
        if DEBUG and _pairing.players()[0].pretty_name() in debug_strategies:
            print(_pairing)
            _pairing.debug()
            print()

    results: typing.List[typing.Dict[str, typing.Any]] = []
    for _strategy in _strategies:

        player_scores = {}
        for _pairing in pairings:
            score = _pairing.score(player=_strategy, first_only=not BOTH_DIRECTIONS)
            if score is not None:
                opponent_name = _pairing.opponent_name(me=_strategy).strip("0123456789")
                player_scores[opponent_name] = (
                    math.ceil((player_scores[opponent_name] + score) / 2)
                    if opponent_name in player_scores
                    else score
                )

        total = sum(score for score in player_scores.values())
        divisor = len(player_scores)

        average = total / divisor
        results.append(
            {
                "name": _strategy.pretty_name(),
                "scores": player_scores,
                "average": average,
            }
        )

    if SORTED:
        results = sorted(results, key=lambda r: r["average"], reverse=True)

    # preserve sort order for horizontal axis
    names = [_result["name"] for _result in results]
    print("".rjust(22) + "  ".join([_result["name"][:3] for _result in results]))

    for _result in results:
        print(
            f"{_result['name'].rjust(20)}: "
            + "  ".join(
                [
                    f"{str(score).rjust(3)}"
                    for score in [
                        _result["scores"][opponent_name]
                        for opponent_name in names
                        if opponent_name in _result["scores"]
                    ]
                ]
            )
            + f"| {_result['average']:.1f}"
        )


# main
if len(sys.argv) > 1:
    ROUNDS = int(sys.argv[1])

ALL_STRATEGIES = [
    strategies.cooperator.Cooperator(),
    strategies.davis.Davis(),
    strategies.downing.Downing(),
    strategies.defector.Defector(),
    strategies.feld.Feld(),
    strategies.friedman.Friedman(),
    strategies.grofman.Grofman(),
    strategies.graaskamp.Graaskamp(),
    strategies.joss.Joss(),
    strategies.name_withheld.NameWithheld(),
    strategies.nydegger.Nydegger(),
    strategies.random.Random(),
    strategies.shubik.Shubik(),
    strategies.stein_and_rapoport.SteinAndRapoport(),
    strategies.downing.RevisedDowning(),
    strategies.tideman_and_chieruzzi.TidemanAndChieruzzi(),
    strategies.titfortat.TitForTat(),
    strategies.titfortwotats.TitForTwoTats(),
    strategies.tullock.Tullock(),
]

TOURNAMENT_ONE_STRATEGIES = [
    strategies.titfortat.TitForTat(),
    strategies.tideman_and_chieruzzi.TidemanAndChieruzzi(),
    strategies.nydegger.Nydegger(),
    strategies.grofman.Grofman(),
    strategies.shubik.Shubik(),
    strategies.stein_and_rapoport.SteinAndRapoport(),
    strategies.friedman.Friedman(),
    strategies.davis.Davis(),
    strategies.graaskamp.Graaskamp(),
    strategies.downing.Downing(),
    strategies.feld.Feld(),
    strategies.joss.Joss(),
    strategies.tullock.Tullock(),
    strategies.name_withheld.NameWithheld(),
    strategies.random.Random(),
]

TEST_STRATEGIES = [
    # strategies.titfortat.TitForTat(),
    # strategies.grofman.Grofman(),
    # strategies.nydegger.Nydegger(),
    strategies.stein_and_rapoport.SteinAndRapoport(),
    strategies.downing.Downing(),
]

simulate(TOURNAMENT_ONE_STRATEGIES, rounds=ROUNDS)
