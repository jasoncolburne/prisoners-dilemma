import strategy

class Defector(strategy.Strategy):
    def cooperate(self, _history) -> bool:
        return False
