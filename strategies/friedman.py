import strategy

class Friedman(strategy.Strategy):
    def cooperate(self, history) -> bool:
        if not all(history.opponent(me=self)):
            return False
        
        return True