# prisoners-dilemma

[Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma).

I focused on reproducing the first tournament of Axelrod's Iterated Prisoner's
Dilemma.

I started on my own and found
[this](https://github.com/Axelrod-Python/Axelrod/blob/dev/axelrod/strategies/axelrod_first.py)
after creating the first few strategies.

I took a lot of ideas from the `axelrod` python implementation, however I found
it did not produce accurate results for the first tournament. I needed to tweak
Downing and Graaskamp in particular, after reading how they were respomnsible for
determining the winners.

It was actually quite hard to make Tit-for-Tat win, I think this may be worthy of
some discussion. The nice strategies still come out on top.

## Simulating a Tournament

```sh
make simulate
```

or 

```sh
make simulate rounds=200
```

## Adding a Strategy

Add a file in the strategies directory. It should conform to the interface defined in
strategy.py (implement cooperate() which should return true to cooperate and false to defect).

To enter the strategy in the tournament, add it to the list at the bottom of main.py
after importing.

Here is a full example:

`strategies/titfortwotats.py`
```python
"""
Tit for two Tats Strategy

This strategy cooperates unless the its opponent defected in both of the most recent
two rounds.
"""

import strategy


class TitForTwoTats(strategy.Strategy):
    """TitForTwoTats Implementation"""

    def cooperate(self, pairing) -> bool:
        opponent_history = pairing.opponent_history(me=self)

        if len(opponent_history) < 2:
            return True

        if not any(opponent_history[-2:]):
            return False

        return True
```

`main.py`
```python
# ...
import strategies.titfortwotats

# ...
simulate(
    [
        strategies.cooperator.Cooperator(),
        strategies.defector.Defector(),
        strategies.friedman.Friedman(),
        strategies.random.Random(),
        strategies.titfortat.TitForTat(),
        strategies.titfortwotats.TitForTwoTats(),
    ],
    rounds=ROUNDS,
)
```
