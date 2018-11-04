import sys

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail

rails = []
for rotation in range(4):
    leftrail = LeftRail(rotation)
    rightrail = RightRail(rotation)
    straightrail = StraightRail(rotation)
    rails.extend([leftrail, rightrail, straightrail])


intersection = Intersection([], rails)
intersection.update()

setup_view = SetupView(intersection=intersection,
                       window_size=(800, 600),
                       x_lanes=2,
                       y_lanes=2)
while not setup_view.done:
    setup_view.tick()
    if setup_view.quitting:
        sys.exit()

kars = setup_view.cars
print("Loading")
intersection2 = Intersection(kars, rails)
intersection2.update()
print(setup_view.lane_cars)

real_actual_view = ZipperView(intersection=intersection2,
                              window_size=(800, 600),
                              x_lanes=2,
                              y_lanes=2)

while not real_actual_view.quitting:
    real_actual_view.tick()
