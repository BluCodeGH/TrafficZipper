import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail


cars = []
rails = []
for rotation in range(4):
    leftrail = LeftRail(rotation)
    rightrail = RightRail(rotation)
    straightrail = StraightRail(rotation)
    rails.extend([leftrail, rightrail, straightrail])
    cars.append(Car(1.0, leftrail))
    cars.append(Car(1.0, rightrail))
    cars.append(Car(1.0, straightrail))
intersection1 = Intersection([], rails)
intersection1.update()
print("Cf", intersection1.cars)

setup_view = SetupView(intersection=intersection1,
                       window_size=(800, 600),
                       x_lanes=2,
                       y_lanes=2)
while not setup_view.done:
    setup_view.tick()

kars = setup_view.cars
intersection1.cars = kars
print(setup_view.lane_cars)

real_actual_view = ZipperView(intersection=intersection1,
                              window_size=(800, 600),
                              x_lanes=2,
                              y_lanes=2)

while 1:
    real_actual_view.tick()
