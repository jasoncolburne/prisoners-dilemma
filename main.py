import random
import sys
import typing

# local
import history
import strategy

# strategies
import strategies.cooperator
import strategies.defector
import strategies.friedman
import strategies.random
import strategies.titfortat

ROUNDS = 200
DEBUG = False

def simulate(strategies: typing.List[strategy.Strategy], rounds: int = ROUNDS) -> None:
    n = 0
    histories: typing.List[history.History] = []
    for strategy in strategies:
        clone = strategy.clone()
        histories.append(history.History(strategy, clone))
        histories.append(history.History(clone, strategy))

        n += 1
        others = strategies[n:]
        for other in others:
            histories.append(history.History(strategy, other))
            histories.append(history.History(other, strategy))
    
    while any([_history.rounds() < rounds for _history in histories]):
        relevant = [_history for _history in histories if _history.rounds() < rounds]
        random.shuffle(relevant)
        relevant[0].create(1)

    for _history in histories:
        print(_history)
        if DEBUG:
            _history.debug()
            print()

    results: typing.List[typing.Dict[str, typing.Any]] = []
    for _strategy in strategies:
        total = sum([score for score in [_history.score(player=_strategy) for _history in histories] if score is not None])
        average = total / len(strategies) / 2
        results.append({"name": _strategy.name(), "average": average})

    print()
    print("summary:")

    for _result in sorted(results, key=lambda r: r["average"], reverse=True):
        print(f"{_result["name"]}: {_result["average"]:.1f}")

# main
rounds = ROUNDS
if len(sys.argv) > 1:
    rounds = int(sys.argv[1])

simulate([
    strategies.cooperator.Cooperator(),
    strategies.defector.Defector(),
    strategies.friedman.Friedman(),
    strategies.random.Random(),
    strategies.titfortat.TitForTat(),
], rounds=rounds)