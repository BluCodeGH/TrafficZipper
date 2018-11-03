import math

from car import Car
from gui import ZipperView, SetupView
from intersection import Intersection
from rail import Rail


def test_rail_fun(pos):
    #print(pos)
    return (pos, 1/(pos+1)*100)


rail1 = Rail(test_rail_fun, 800)
car1 = Car(1.0, rail1, 1)
car2 = Car(2.0, rail1, 2)
intersection1 = Intersection([car1, car2], [rail1])

view = SetupView(intersection=intersection1,
                  window_size=(800, 600),
                  x_lanes=4,
                  y_lanes=4)
while 1:
    view.tick()
