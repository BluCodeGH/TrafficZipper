import math
from rail import Rail


class Car:
    def __init__(self, start_speed: float, rail: Rail, priority: int, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.position = 0.0
        self.accells = accells or [(rail.max_position, 0)]
        self.priority = priority

    def get_pos(self, time):
        scalar = 0
        speed = self.start_speed
        found = False
        i = 0
        while not found:
            print(i)
            a = self.accells[i][1]
            if i == 0:
                d = self.accells[i][0]
            else:
                d = self.accells[i][0] - self.accells[i - 1][0]
            v2 = math.sqrt(speed**2 + 2 * a * d)
            print("v", v2)
            if speed + v2 != 0:
                t = 2 * d / (speed + v2)
            else:
                t = 0
            print("t", t)
            if t > time:
                found = True
                scalar += time * (speed + 0.5*a*time)
            else:
                time -= t
                print("T", time)
                speed = speed + a * t
                print("S", speed)
                scalar = self.accells[i][0]
            i += 1
        return scalar
