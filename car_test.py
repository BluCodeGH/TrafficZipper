from car import Car
from intersection import Intersection
from rail import Rail

def fun(x):
    return x - 50, 0

def fun2(x):
    return 0, x - 50

def fun3(x):
    return 77, x - 100

r = Rail(fun, 200)
r2 = Rail(fun2, 200)
r3 = Rail(fun3, 200)


c = Car(10, r, 1, [(50, 0), (150, 0)])
c2 = Car(10, r2, 2, [(50, 0), (150, 0)])
c3 = Car(10, r3, 3, [(200, 0)])

_=2

i = Intersection([c2, c, c3], [r, r2, r3])

if __name__ == '__main__':
    i.update()
