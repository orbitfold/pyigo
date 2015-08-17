from pyigo.pyigo import optimize
from interval.imath import *
from interval import interval

def rastrigin(xs, offsets):
    return 10.0 * len(xs) + sum([x ** 2 - 10.0 * cos(2.0 * pi * x) for x in xs])

if __name__ == '__main__':
    optimize(rastrigin, [[interval([-5.12, 5.12])] * 10])
