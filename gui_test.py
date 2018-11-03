import math

from car import Car
from gui import ZipperView
from intersection import Intersection
from rail import Rail


def test_rail_fun(pos):
    #print(pos)
    return (pos, 1/(pos+1)*100)


rail1 = Rail(test_rail_fun)
car1 = Car(1.0, rail1, 1)
car2 = Car(2.0, rail1, 2)
intersection1 = Intersection([car1, car2], [rail1])

view = ZipperView(intersection=intersection1,
                  window_size=(800, 400),
                  x_lanes=2,
                  y_lanes=2)
while 1:
    view.tick()
