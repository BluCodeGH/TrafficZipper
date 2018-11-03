import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail, LeftRail, RightRail, StraightRail


def test_rail_fun(pos):
    #print(pos)
    return (pos, 1/(pos+1)*100)

rail0 = Rail(test_rail_fun)
rail1 = LeftRail(0)
rail2 = RightRail(0)
rail3 = StraightRail(0)
car1 = Car(1.0, rail1, 1)
car2 = Car(1.0, rail2, 2)
car3 = Car(1.0, rail3, 3)
intersection1 = Intersection([car1, car2, car3], [rail1])

view = ZipperView(intersection=intersection1,
                  window_size=(800, 600),
                  x_lanes=2,
                  y_lanes=2)
while 1:
    view.tick()
