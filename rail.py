class Rail:
    def __init__(self, fun):
        self.fun = fun

    def get(self, i):
        return self.fun(i)
