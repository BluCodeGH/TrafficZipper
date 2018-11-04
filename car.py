import math
from rail import Rail

max_acceleration = 1


class Car:
    def __init__(self, start_speed: float, rail: Rail, name, start_time=0, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.name = name
        # Each element is a tuple containing the end position of the car (i.e. when the car changes its acceleration),
        # and the acceleration of the car during that interval.
        self.accells = accells or [(self.rail.total_distance, 0.1)]
        self.accellsI = 0
        self.radius = 25   # TODO:  Change this if necessary
        self.start_time = start_time

    def get_location(self, time):
        """
        Returns the (x, y) location of the car at a certain time.
        """
        return self.rail.get(self.get_pos(time))

    def get_interval(self, time):
        """
        This takes a single time argument.

        This returns a bunch of internal information about the *start of the acceleration range the car is in at a given
        time*.
        This does *not* account for the car's position within the acceleration range.
        It returns: 
            the index of the range (or None if the car has passed out of all ranges, in which case it is assumed to have
                zero acceleration)
            the distance covered by the range
            the speed the car starts the range with
            the acceleration during the range
            the time the car has spent in the range
        """
        if time < self.start_time:
            return 0, 0, 0, 0, 0
        time -= self.start_time
        speed = self.start_speed
        accells = self.accells
        i = 0
        while True:
            if i == len(accells):
                return None, 0, speed, 0, time
            a = accells[i][1]
            if i == 0:
                d = accells[i][0]
            else:
                d = accells[i][0] - accells[i - 1][0]
            v2 = math.sqrt(speed**2 + 2 * a * d)
            t = 2 * d / (speed + v2)
            if t > time:
                return i, d, speed, a, time
            else:
                time -= t
                speed = speed + a * t
            i += 1

    def get_pos(self, time):
        """
        This function takes a time and returns the scalar value of the car along its rail at that time.
        """
        if time < self.start_time:
            return 0
        i, d, speed, a, time = self.get_interval(time)
        if i is None:
            scalar = self.accells[-1][0]
        elif i > 0:
            scalar = self.accells[i - 1][0]
        else:
            scalar = 0
        v2 = math.sqrt(speed**2 + 2 * a * d)
        scalar += (speed + v2) / 2 * time
        return scalar

    def get_time(self):
        """
        This function returns the time at which the car has completed all of its acceleration ranges, and is 
        assumed to be cruising at a constant velocity after leaving the intersection.
        """
        time = self.start_time
        speed = self.start_speed
        oldD = 0
        for d, a in self.accells:
            d -= oldD
            v2 = math.sqrt(speed**2 + 2 * a * d)
            t = 2 * d / (speed + v2)
            time += t
            speed = v2
        return time

    def copy(self):
        """
        This copies a car
        """
        return Car(self.start_speed, self.rail, self.name, start_time=self.start_time, accells=self.accells.copy())

    def __repr__(self):
        res = self.name + "[("
        for d, a in self.accells:
            res += str(round(d)) + "," + str(a) + ")("
        return res + "]"
