from rail import *
from intersection import *
from car import *


def getRail(transform, value):
    if value == 0:
        return LeftRail(transform)
    elif value == 1:
        return StraightRail(transform)
    else:
        return RightRail(transform)

# cars data is formatted speed,railNum,priority
# rails data is formatted transform,type
if __name__ == "__main__":
    rails_dict = {1: ""}

    railsFile = open("assets/rails.txt")
    railsData = railsFile.readlines()

    carsFile = open("assets/cars.txt")
    carsData = carsFile.readlines()

    rails = []
    for item in railsData:
        item = item.strip()
        value = item.split(",")

        rails.append(getRail(value[0], value[1]))

    cars = []
    for item in carsData:
        item = item.strip()
        value = item.split(",")

        cars.append(Car(int(value[0]), rails[int(value[1]) - 1], start_time=int(value[2])))

    intersection = Intersection(cars, rails)
    intersection.update()
