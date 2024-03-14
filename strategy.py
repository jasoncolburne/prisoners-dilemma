import random


class Strategy:
    def __init__(self):
        self._name = f"{self.__class__.__name__}{random.randint(0,9999)}"

    def name(self):
        return self._name

    def cooperate(self, history) -> bool:
        raise Exception("unimplemented")

    def clone(self):
        return self.__class__()
