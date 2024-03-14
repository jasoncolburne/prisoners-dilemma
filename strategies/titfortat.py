import strategy

class TitForTat(strategy.Strategy):
    def cooperate(self, history) -> bool:
        opponent_history = history.opponent(me=self)
        
        if len(opponent_history) == 0:
            return True
        
        if not opponent_history[-1]:
            return False
        
        return True
