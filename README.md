# prisoners-dilemma

[Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma).

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

    def cooperate(self, history) -> bool:
        opponent_history = history.opponent(me=self)

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
