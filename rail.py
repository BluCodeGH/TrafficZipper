class Rail:
    def __init__(self, fun):
        self.fun = fun

    def get(self, position):
        return self.fun(position)
