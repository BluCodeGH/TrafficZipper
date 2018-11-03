import math
from rail import Rail


class Car:
    def __init__(self, start_speed: float, rail: Rail, priority: int, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.position = 0.0
        self.accells = accells or [(rail.max_position, 0)]
        self.priority = priority

    def get_interval(self, time):
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
        return Car(self.start_speed, self.rail, self.priority, self.accells.copy())
