"""
Main
"""

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


def simulate(
    _strategies: typing.List[strategy.Strategy],
    rounds: int = ROUNDS,
    debug_strategies: typing.List[str] = [],
) -> None:
    """Simulates the classic prisoner's dilemma tournament"""

    n = 0
    pairings: typing.List[pairing.Pairing] = []
    for _strategy in _strategies:
        twin = _strategy.clone()
        pairings.append(pairing.Pairing(_strategy, twin))
        pairings.append(pairing.Pairing(twin, _strategy))

        n += 1
        others = _strategies[n:]
        for other in others:
            pairings.append(pairing.Pairing(_strategy, other))
            pairings.append(pairing.Pairing(other, _strategy))

    while any(_pairing.rounds() < rounds for _pairing in pairings):
        relevant = [_pairing for _pairing in pairings if _pairing.rounds() < rounds]
        random.shuffle(relevant)
        relevant[0].create(1)

    for _pairing in pairings:
        if DEBUG and _pairing._players[0].pretty_name() in debug_strategies:
            print(_pairing)
            _pairing.debug()
            print()

    results: typing.List[typing.Dict[str, typing.Any]] = []
    for _strategy in _strategies:
        player_scores = [
            score
            for score in [
                _pairing.score(player=_strategy, first_only=True)
                for _pairing in pairings
            ]
            if score is not None
        ]
        total = sum(player_scores)
        average = total / len(_strategies)
        results.append(
            {
                "name": _strategy.pretty_name(),
                "scores": player_scores,
                "average": average,
            }
        )

    print()

    if SORTED:
        results = sorted(results, key=lambda r: r["average"], reverse=True)

    print("".rjust(22) + "  ".join([_result["name"][:3] for _result in results]))
    for _result in results:
        print(
            f"{_result['name'].rjust(20)}: {'  '.join([f'{str(score).rjust(3)}' for score in _result['scores']])} | {_result['average']:.1f}"
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
