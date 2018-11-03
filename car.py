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
        self.radius = 10   # TODO:  Change this if necessary

    def __iadd__(self, other: int):
        self.position += self.speed * other

    def get_location(self, new_position):
        return self.rail.fun(new_position)
