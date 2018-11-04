import math
import random

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection, distance
from rail import Rail, LeftRail, RightRail, StraightRail


cars = []
rails = []
for rotation in range(0, 4):
    leftrail = LeftRail(rotation)
    rightrail = RightRail(rotation)
    straightrail = StraightRail(rotation)
    rails.extend([leftrail, rightrail, straightrail])
#     #rails.append(leftrail)
#     cars.append(Car(1.0, leftrail, "CAR0",start_time=5))
#     #cars.append(Car(1.0, rightrail, "CAR1"))
#     cars.append(Car(1.0, straightrail, "CAR2"))
intersection1 = Intersection(cars, rails)
print(intersection1.rails)
intersection1.update()
# print("Cf", intersection1.cars)

#rails2 = [LeftRail(0), LeftRail(1), LeftRail(2)]

# intersection2 = Intersection([
#   Car(1.0, rails2[0], 0, [(133, 1.0), (163, 0.1), (184, 0.1), (318, 0.1)]),
#   Car(1.0, rails2[1], 0, [(155, 0.1), (163, 0.1), (318, 0.1)]),
#   Car(1.0, rails2[2], 0, [(134, 0.2), (155, 0.1), (184, 0.1), (318, 0.1)]),], rails2)

# setup_view = SetupView(intersection=intersection1,
#                        window_size=(800, 600),
#                        x_lanes=2,
#                        y_lanes=2)
# while not setup_view.done:
#     setup_view.tick()

# kars = setup_view.cars
# intersection1.cars = kars
# print(setup_view.lane_cars)

view = ZipperView(intersection=intersection1,
                              window_size=(800, 600),
                              x_lanes=6,
                              y_lanes=6)

j = 0
while not view.quitting:
    view.tick()
    for i, car in enumerate(intersection1.cars):
        if car.get_pos(view.time) > car.rail.total_distance:
            intersection1.cars.pop(i)

    if random.randint(0, 100) < 100:
        randRail = random.randint(0, 11)
        car = Car(1, intersection1.rails[randRail], "CAR" + str(j), start_time=view.time)
        bad = False
        for c2 in intersection1.cars:
            if distance(c2.get_location(view.time), car.get_location(view.time)) < car.radius * 2:
                bad = True
            if c2.rail == car.rail:
                bad = True
        if bad:
            continue
        j += 1
        intersection1.split([car])
        intersection1.cars.append(car)

        intersection1.update()


