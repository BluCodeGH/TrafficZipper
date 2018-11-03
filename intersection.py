from typing import List

from car import Car
from rail import Rail


class Intersection:
    def __init__(self, cars: List[Car], rails: List[Rail]):
        self.cars = cars
        self.rails = rails
