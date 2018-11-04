from typing import List, Tuple
import math

from car import Car, max_acceleration
from rail import Rail


class Intersection:
    def __init__(self, cars: List[Car], rails: List[Rail], cl=None):
        self.cars = cars
        self.rails = rails
        self.collisions_dict = cl or {}
        if not cl:
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
        
        for rail_a in self.rails:
            for rail_b in self.rails:
                if rail_a != rail_b:
                    if self.collisions_dict[rail_a][rail_b]:
                        # We have already filled in this dictionary entry.
                        continue
                    scalar_a, scalar_b = self.find_intersection(rail_a, rail_b)
                    if scalar_a >= 0:
                        # If the rails don't collide, the dictionary value stays at 0.
                        self.collisions_dict[rail_a][rail_b] = scalar_a
                        self.collisions_dict[rail_b][rail_a] = scalar_b

        for car in self.cars:
            for rail_b, d in self.collisions_dict[car.rail].items():
                if d is not None:
                    car.accells.append((d, 0.1))
            print(car.accells)
            car.accells.sort(key=lambda x: x[0])

    def update(self):
        """
        iterate and check with all other cars, handle() at first coll.
        """
        for i in range(len(self.cars) - 1):
            # This will contain the indices of the rails that self.rails[i] will collide with.
            collision_car_indices = []
            car_1 = self.cars[i]
            for j in range(i + 1, len(self.cars)):
                car_2 = self.cars[j]
                if self.collisions_dict[car_1.rail][car_2.rail]:
                    collision_car_indices.append(j)

            collision_car_indices.sort(key=lambda x: self.collisions_dict[self.cars[i].rail][self.cars[x].rail])

            for j in collision_car_indices:
                car_2 = self.cars[j]
                collision_time = self.collision(car_1, car_2)
                if collision_time >= 0:
                    print("Coll between", car_1, car_2)
                    _, _, speed_1, acc_1, time_1 = car_1.get_interval(collision_time)
                    _, _, speed_2, acc_2, time_2 = car_2.get_interval(collision_time)

                    # Get the speeds that each car will have at the time they collide.
                    speed_1_coll_time = speed_1 + acc_1 * time_1
                    speed_2_coll_time = speed_2 + acc_2 * time_2
                    if speed_2_coll_time >= speed_1_coll_time:
                        # car_1 has the greater speed at the collision time, so it should be the accelerator.
                        try:
                            c = self.cars.copy()
                            self.handle(i, j, collision_time)
                        except ValueError:
                            self.cars = c
                            self.handle(j, i, collision_time)
                    else:
                        # car_2 has the greater speed at the collision time, so it should be the accelerator.
                        try:
                            c = self.cars.copy()
                            self.handle(j, i, collision_time)
                        except ValueError:
                            self.cars = c
                            self.handle(i, j, collision_time)
                    return

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
            a2 += 0.001
            newA.accells[i] = (newA.accells[i][0], a2)


        newD = carD.copy()
        print(newD, time)
        i, dist, speed, a, dt = newD.get_interval(time)
        a2 = a
        while a2 >= -max_acceleration:
            newD.accells[i] = (newD.accells[i][0], a2)
            if self.collision(newD, newA) == -1:
                break
            a2 -= 0.001

        print("got cars:", newA.accells, newD.accells)

        self.cars[carAi] = newA
        self.cars[carDi] = newD
        print(self.cars)
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

    def find_intersection(self, rail_1, rail_2):
        """
        Given two rails, returns the point of intersection, or None if they do not intersect.

        :param rail_1:
        :param rail_2:
        :return: The point of intersection of rail_1 and rail_2, or None if they don't intersect.
        """
        min_dist = None
        min_steps = 0.0, 0.0
        step_1 = 0
        while step_1 < rail_1.total_distance:
            step_2 = 0
            while step_2 < rail_2.total_distance:
                rail_dist = distance(rail_1.get(step_1), rail_2.get(step_2))
                if min_dist is None or rail_dist < min_dist:
                    min_dist = rail_dist
                    min_steps = step_1, step_2
                step_2 += 1
            step_1 += 1
        return min_steps if min_dist < 1 else (-1, -1)


def distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    """
    Returns the distance between two (x, y) locations.
    """
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
