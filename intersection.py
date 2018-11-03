from typing import List
import math
from car import Car
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

    def collision(self, index_1: int, index_2: int):
        """
        Returns whether or not self.cars[index_1] and self.cars[index_2] will intersect.

        :param index_1: The index of the first car.
        :param index_2: The index of the second car.
        :return: True iff self.cars[index_1] and self.cars[index_2] will intersect.
        """
        car_1 = self.cars[index_1]
        car_2 = self.cars[index_2]
        car_1_time_to_end = car_1.speed * (car_1.rail.max_position - car_1.position)
        car_2_time_to_end = car_2.speed * (car_2.rail.max_position - car_2.position)
        if car_1_time_to_end > car_2_time_to_end:
            self.step_through_time(car_1, car_2)
        else:
            self.step_through_time(car_2, car_1)

    def step_through_time(self, car_1, car_2):
        """
        Steps through time and figures out whether the two given cars will collide.

        :param car_1:
        :param car_2:
        :return: True iff the cars will eventually collide, if their speeds don't change.
        """
        prev_dist_between_cars = None

        # Loop until car_1 is at the end of its rail.
        for time_ticks in range(car_1.speed * (car_1.rail.max_position - car_1.position)):
            car_1_pos = car_1.get_location(car_1.position + car_1.speed * time_ticks)
            car_2_pos = car_2.get_location(car_2.position + car_2.speed * time_ticks)
            curr_dist_between_cars = self.distance(car_1_pos, car_2_pos)
            if curr_dist_between_cars < car_1.radius + car_2.radius:
                return True
            # Break if the distance between the cars is increasing.
            if prev_dist_between_cars and prev_dist_between_cars < curr_dist_between_cars:
                break
            prev_dist_between_cars = curr_dist_between_cars
        return False

def distance(pos_1, pos_2):
    """
    Returns the distance between two (x, y) locations.
    """
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
