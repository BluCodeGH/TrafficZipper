import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail


def test_rail_fun(pos):
    #print(pos)
    return (pos, 1/(pos+1)*100)

# rail0 = Rail(test_rail_fun)
# rail1 = LeftRail(0)
# rail2 = LeftRail(1)
# rail3 = LeftRail(2)
# rail4 = LeftRail(3)
# car1 = Car(1.0, rail1, 1)#, [(50, 0.01), (100, -0.01)])
# car2 = Car(1.0, rail2, 2)#, [(400, 0.2), (900, -0.3)])
# car3 = Car(1.0, rail3, 3)
# car4 = Car(1.0, rail4, 4)
# intersection1 = Intersection([car1, car2, car3, car4], [rail1])


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
intersection1 = Intersection(cars, rails)

setup_view = SetupView(intersection=intersection1,
                       window_size=(800, 600),
                       x_lanes=2,
                       y_lanes=2)
while not setup_view.done:
    setup_view.tick()

kars = setup_view.cars
intersection1.cars = kars

real_actual_view = ZipperView(intersection=intersection1,
                              window_size=(800, 600),
                              x_lanes=2,
                              y_lanes=2)

while 1:
    real_actual_view.tick()
