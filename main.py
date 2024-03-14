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

def simulate(strategies: typing.List[strategy.Strategy], rounds: int = ROUNDS) -> None:
    n = 0
    histories: typing.List[history.History] = []
    for strategy in strategies:
        n += 1
        clone = strategy.clone()
        histories.append(history.History(strategy, clone))
        histories.append(history.History(clone, strategy))
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
        _history.debug()
        print()


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