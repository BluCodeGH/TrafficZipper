from rail import *
from intersection import *
from car import *
from gui import ZipperView


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

        rails.append(getRail(int(value[0]), int(value[1])))

    cars = []
    for index, item in enumerate(carsData):
        item = item.strip()
        value = item.split(",")

        dir_str = ""
        if int(value[1]) % 3 == 0:
            dir_str = " RIGHT"
        elif int(value[1]) % 3 == 1:
            dir_str = " LEFT"
        else:
            dir_str = " STRAIGHT"

        cars.append(Car(int(value[0]), rails[int(value[1]) - 1], "car" + str(index) + dir_str, start_time=int(value[2])))

    intersection = Intersection(cars, rails)
    intersection.update()

    real_actual_view = ZipperView(intersection=intersection,
                                  window_size=(800, 600),
                                  x_lanes=2,
                                  y_lanes=2)

    while 1:
        real_actual_view.tick()
