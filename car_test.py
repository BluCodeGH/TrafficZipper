from car import Car
from intersection import Intersection
from rail import Rail

def fun(x):
    return x - 50, 0

def fun2(x):
    return 0, x - 50

def fun3(x):
    return 77, x - 100

c = Car(10, Rail(fun), 1, [(50, 0), (150, 0)])
c2 = Car(10, Rail(fun2), 2, [(50, 0), (150, 0)])
c3 = Car(10, Rail(fun3), 3, [(200, 0)])

_=5

i = Intersection([c, c2, c3], [])

if __name__ == '__main__':
    i.update()
