import math
from rail import Rail

max_acceleration = 0.5


class Car:
    def __init__(self, start_speed: float, rail: Rail, priority: int, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.position = 0.0
        # Each element is a tuple containing the end position of the car (i.e. when the car changes its acceleration),
        # and the acceleration of the car during that interval.
        self.accells = accells or [(0, 0)]
        self.priority = priority
        self.radius = 3   # TODO:  Change this if necessary

    def update(self, others):
        for other in others:
            collision_time = self.collision(self, other)
            if collision_time >= 0:
                print("Coll between", self, other)
                _, _, speed_1, acc_1, time_1 = self.get_interval(collision_time)
                _, _, speed_2, acc_2, time_2 = other.get_interval(collision_time)

                # Get the speeds that each car will have at the time they collide.
                speed_1_coll_time = speed_1 + acc_1 * time_1
                speed_2_coll_time = speed_2 + acc_2 * time_2
                if speed_2_coll_time >= speed_1_coll_time:
                    # self has the greater speed at the collision time, so it should be the accelerator.
                    self.handleAcc(other, collision_time)
                else:
                    # other has the greater speed at the collision time, so it should be the accelerator.
                    other.handleAcc(self, collision_time)
                return

    def handleAcc(self, other, time):
        

    def collision(self, carB: Car):
        """
        This returns whether or not two cars are going to collide.
        """
        time = min(self.get_time(), carB.get_time())
        t = 0
        while t <= time:
            a = self.get_location(t)
            b = carB.get_location(t)
            if distance(a, b) < self.radius + carB.radius:
                return t
            t += 0.1
        return -1

    def get_location(self, time):
        """
        Returns the (x, y) location of the car at a certain time.
        """
        return self.rail.fun(self.get_pos(time))

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
        return Car(self.start_speed, self.rail, self.priority, self.accells.copy())

    def __repr__(self):
        return str(self.priority) + ":" + str(self.accells)

def distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    """
    Returns the distance between two (x, y) locations.
    """
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
