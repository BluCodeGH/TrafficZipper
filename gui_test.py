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

rails2 = [LeftRail(0), LeftRail(1), LeftRail(2)]

intersection2 = Intersection([
  Car(1.0, rails2[0], 0, [(133, 1.0), (163, 0.1), (184, 0.1), (318, 0.1)]),
  Car(1.0, rails2[1], 0, [(155, 0.1), (163, 0.1), (318, 0.1)]),
  Car(1.0, rails2[2], 0, [(134, 0.2), (155, 0.1), (184, 0.1), (318, 0.1)]),], rails2)

# setup_view = SetupView(intersection=intersection1,
#                        window_size=(800, 600),
#                        x_lanes=2,
#                        y_lanes=2)
# while not setup_view.done:
#     setup_view.tick()

# kars = setup_view.cars
# intersection1.cars = kars
# print(setup_view.lane_cars)

real_actual_view = ZipperView(intersection=intersection2,
                              window_size=(800, 600),
                              x_lanes=2,
                              y_lanes=2)

while 1:
    real_actual_view.tick()
