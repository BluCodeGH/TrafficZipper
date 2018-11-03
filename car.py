from rail import Rail


class Car:
    def __init__(self,
                 speed: float,
                 rail: Rail,
                 priority: int):
        self.speed = speed
        self.rail = rail
        self.position = 0.0
        self.priority = priority

    def __iadd__(self, other: int):
        self.position += self.speed * other
