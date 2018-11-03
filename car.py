import math
from rail import Rail

max_acceleration = 2


class Car:

    def __init__(self, start_speed: float, rail: Rail, priority: int, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.position = 0.0
        # Each element is a tuple containing the end position of the car (i.e. when the car changes its acceleration),
        # and the acceleration of the car during that interval.
        self.accells = accells or [(rail.max_position, 0)]
        self.priority = priority
        self.radius = 10   # TODO:  Change this if necessary

    def get_location(self, new_position=None):
        """
        Returns the (x, y) location of the car at new_position if it's specified, or at the car's position otherwise.
        """
        return self.rail.fun(new_position or self.position)

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
        scalar = 0
        speed = self.start_speed
        found = False
        i = 0
        while not found:
            if i == len(self.accells):
                return None, 0, speed, 0, time
            a = self.accells[i][1]
            if i == 0:
                d = self.accells[i][0]
            else:
                d = self.accells[i][0] - self.accells[i - 1][0]
            v2 = math.sqrt(speed**2 + 2 * a * d)
            if speed + v2 != 0:
                t = 2 * d / (speed + v2)
            else:
                t = 0
            if t > time:
                return i, d, speed, a, time
            else:
                time -= t
                speed = speed + a * t
                scalar = self.accells[i][0]
            i += 1
        return None

    def get_pos(self, time):
        """
        This function takes a time and returns the scalar value of the car along its rail at that time.
        """
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
        time = 0
        speed = 0
        oldD = 0
        for d, a in self.accells:
            d -= oldD
            v2 = math.sqrt(speed**2 + 2 * a * d)
            if speed + v2 != 0:
                t = 2 * d / (speed + v2)
            else:
                t = 0
            time += t
            speed = v2
        return time

    def copy(self):
        """
        This copies a car
        """
        return Car(self.start_speed, self.rail, self.priority, self.accells.copy())
