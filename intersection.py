from typing import List, Tuple
import math

from car import Car, max_acceleration
from rail import Rail


class Intersection:
    def __init__(self, cars: List[Car], rails: List[Rail]):
        self.cars = cars
        self.rails = rails
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

    def update(self):
        """
        iterate and check with all other cars, handle() at first coll.
        """
        for i in range(len(self.cars) - 1):
            for j in range(i + 1, len(self.cars)):
                car_1 = self.cars[i]
                car_2 = self.cars[j]
                collision_time = self.collision(car_1, car_2)
                print(collision_time)
                if collision_time >= 0:
                    _, _, speed_1, acc_1, time_1 = car_1.get_interval(collision_time)
                    _, _, speed_2, acc_2, time_2 = car_2.get_interval(collision_time)

                    # Get the speeds that each car will have at the time they collide.
                    speed_1_coll_time = speed_1 + acc_1 * time_1
                    speed_2_coll_time = speed_2 + acc_2 * time_2
                    if speed_2_coll_time < speed_1_coll_time:
                        # car_1 has the greater speed at the collision time, so it should be the accelerator.
                        self.handle(i, j, collision_time)
                    else:
                        # car_2 has the greater speed at the collision time, so it should be the accelerator.
                        self.handle(j, i, collision_time)
                    break

    def handle(self, carAi, carDi, time):
        """
        This function stops two cars from colliding.
        carA is the car to accelerate
        carD is the car to decelerate
        time is the time of the collision

        It works by first changing carAs last acceleration (before the collision) so it arrives on the intersection at
        the time.
        Next it iteratively slows carD until they do not hit at the intersection.

        TODO:
        This should then call update with the changed cars in order to propagate the changes.
        It should return the total amount of speed changes so its parent update can optimize which car slows
        down / speeds up.
        """
        carA = self.cars[carAi]
        carD = self.cars[carDi]

        a_dist = 60  # self.I[carA.rail][carD.rail]
        d_dist = 60  # self.I[carD.rail][carA.rail]

        i, dist, speed, a, dt = carA.get_interval(time)
        a2 = a
        newA = carA.copy()
        while a2 < max_acceleration and self.collision(carD, newA) != -1:
            a2 += 0.1
            newA.accells[i] = (newA.accells[i][0], a2)


        newD = carD.copy()
        i, dist, speed, a, dt = newD.get_interval(time)
        a2 = a
        while a2 >= -max_acceleration:
            print(a2)
            newD.accells[i] = (newD.accells[i][0], a2)
            print(newD.get_pos(time))
            if self.collision(newD, newA) == -1:
                break
            a2 -= 0.1

        self.cars[carAi] = newA
        self.cars[carDi] = newD
        self.update()

    def collision(self, carA: Car, carB: Car):
        """
        This returns whether or not two cars are going to collide.
        """
        time = min(carA.get_time(), carB.get_time())
        t = 0
        while t <= time:
            a = carA.get_location(t)
            b = carB.get_location(t)
            if distance(a, b) < carA.radius + carB.radius:
                return t
            t += 0.1
        return -1


def distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    """
    Returns the distance between two (x, y) locations.
    """
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
