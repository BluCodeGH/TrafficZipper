from typing import List, Tuple
import math

from car import Car
from rail import Rail


class Intersection:
    def __init__(self, cars: List[Car], rails: List[Rail]):
        self.cars = cars
        self.rails = rails
        self.I = {}
        self.collisions_dict = {}
        self.init_collisions_dict()

    def init_collisions_dict(self):
        """
        Initializes the dictionary of collision points between
        rails, setting each value to None.
        """
        for rail_a in self.rails:
            self.collisions_dict[rail_a] = {}
            for rail_b in self.rails:
                if rail_a != rail_b:
                    self.collisions_dict[rail_a][rail_b] = None

    def update(self, cars):
        """
        iterate and check with all other cars, handle() at first coll.
        """
        for car_1 in self.cars:
            for car_2 in self.cars:
                if car_1 != car_2 and self.collision(car_1, car_2):
                    pass

    def handle(self, carA, carD, time):
        """
        get dists to intersect for cars
        update cA accel to be centered
        update cB accel to never touch cA
        call update with new cars
        """
        a_dist = 60  # self.I[carA.rail][carD.rail]
        d_dist = 60  # self.I[carD.rail][carA.rail]
        i, dist, speed, a, dt = carA.get_interval(time)
        a2 = 2 * (a_dist - speed * dt) / (dt ** 2)
        newA = carA.copy()
        newA.accells[i] = (newA.accells[i][0], a2)

        newD = carD.copy()
        i, dist, speed, a, dt = newD.get_interval(time)
        a2 = a
        while a2 >= -5:
            print(a2)
            newD.accells[i] = (newD.accells[i][0], a2)
            print(newD.get_pos(time))
            if not self.collision(newD, newA):
                break
            a2 -= 0.1

        print(newD.accells, newA.accells)

    def collision(self, carA, carB):
        time = min(carA.get_time(), carB.get_time())
        t = 0
        while t <= time:
            a = carA.rail(carA.get_pos(t))
            b = carB.rail(carB.get_pos(t))
            if math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) < 10:
                print(a, b)
                return True
            t += 0.1
        return False


def distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    """
    Returns the distance between two (x, y) locations.
    """
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
