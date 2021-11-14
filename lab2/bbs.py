class Bbs:
    def __init__(self, p1, p2, seed):
        self.m = p1 * p2
        self.x = seed

    def next(self):
        self.x = (self.x ** 2) % self.m
        return self.x