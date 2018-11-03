from typing import Callable


class Rail:
    def __init__(self, fun: Callable, max_position: int):
        self.fun = fun
        self.max_position = max_position

    def get(self, position: float):
        return self.fun(position)
