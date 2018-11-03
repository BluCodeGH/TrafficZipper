class Intersection:
    def __init__(self, cars):
        self.cars = cars
        self.init_collisions_dict()

    def init_collisions_dict(self):
        self.collisions_dict = {}

    def collision(self, index_1, index_2):
        car_1 = self.cars[index_1]
        car_2 = self.cars[index_2]
