import strategy


class Cooperator(strategy.Strategy):
    def cooperate(self, _history) -> bool:
        return True
