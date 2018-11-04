import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail


cars = []
rails = []
for rotation in range(4):
    leftrail = LeftRail(rotation)
    #rightrail = RightRail(rotation)
    #straightrail = StraightRail(rotation)
    #rails.extend([leftrail, rightrail, straightrail])
    rails.append(leftrail)
    cars.append(Car(1.0, leftrail))
    #cars.append(Car(1.0, rightrail))
    #cars.append(Car(1.0, straightrail))
intersection1 = Intersection(cars, rails)

#straightrail = StraightRail(0)
#leftrail = LeftRail(3)
#intersection1 = Intersection([Car(1.0, straightrail, [(200, 0), (200, 0)]), Car(1.0, leftrail, [(218, 0), (200, 0)])], [straightrail, leftrail])
#intersection1 = Intersection([Car(1.0, straightrail), Car(1.0, leftrail)], [straightrail, leftrail])
#print(intersection1.collisions_dict)
intersection1.update()
print("Cf", intersection1.cars)
#setup_view = SetupView(intersection=intersection1,
#                       window_size=(800, 600),
#                       x_lanes=2,
#                       y_lanes=2)
#while not setup_view.done:
#    setup_view.tick()

#kars = setup_view.cars
#intersection1.cars = kars

real_actual_view = ZipperView(intersection=intersection1,
                              window_size=(800, 600),
                              x_lanes=2,
                              y_lanes=2)

while 1:
    real_actual_view.tick()
