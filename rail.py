from typing import Callable


class Rail:
    def __init__(self, fun: Callable):
        self.fun = fun

    def get(self, position: float):
        return self.fun(position)
