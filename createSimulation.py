if __name__ == "__main__":
    file = open("rails.txt")
    data = file.readlines()

    rails = []
    for item in data:
        item.split(",")
        print(item)
