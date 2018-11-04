import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail


cars = []
rails = []
for rotation in range(0, 3):
    leftrail = LeftRail(rotation)
    #rightrail = RightRail(rotation)
    #straightrail = StraightRail(rotation)
    #rails.extend([leftrail, rightrail, straightrail])
    rails.append(leftrail)
    cars.append(Car(1.0, leftrail, "CAR" + str(rotation)))
    #cars.append(Car(1.0, rightrail))
    #cars.append(Car(1.0, straightrail))
#intersection1 = Intersection(cars, rails)

rails2 = [LeftRail(0), LeftRail(1), LeftRail(2)]

cars = [
  Car(1.0, rails2[0], 0),
  Car(1.0, rails2[1], 0),
  Car(1.0, rails2[2], 0)]

intersection1 = Intersection(cars, rails2, False)
cars[0].accells = [(133, 0.6), (163, 0.6), (184, 0.1), (318, 0.1)]
cars[1].accells = [(155, 0.2), (163, 0.1), (318, 0.1)]
cars[2].accells = [(134, 0.1), (155, 0.1), (184, 0.1), (318, 0.1)]

#straightrail = StraightRail(0)
#leftrail = LeftRail(3)
#intersection1 = Intersection([Car(1.0, straightrail, [(200, 0), (200, 0)]), Car(1.0, leftrail, [(218, 0), (200, 0)])], [straightrail, leftrail])
#intersection1 = Intersection([Car(1.0, straightrail), Car(1.0, leftrail)], [straightrail, leftrail])
#print(intersection1.collisions_dict)
#intersection1.update()
#print("Cf", intersection1.cars)
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
