class Car:
    def __init__(self, length, width, initial_speed, priority):
        self.length = length
        self.width = width
        self.speed = initial_speed
        # The car's position is the scalar representing how far along the rail we are.
        self.position = 0
        self.priority = priority
