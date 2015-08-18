import numpy as np
from interval import interval, imath
import itertools

def solve(fn, intervals, deriv1=None, deriv2=None, verbose=True):
    best = [None]
    best_x = [None]
    intervals = [[interval(inter) for inter in intervals]]
    def optimizer(intervals, iterations):
        for iteration in range(iterations):
            mid = [inter.midpoint for inter in intervals[0]]
            mid_y = fn(mid)
            if best[0] is None or mid_y < best[0]:
                best[0] = mid_y
                best_x[0] = mid
            split1 = [interval([inter[0][0], inter.midpoint]) for inter in intervals[0]]
            split2 = [interval([inter.midpoint, inter[0][1]]) for inter in intervals[0]]
            split = zip(split1, split2)
            products = list(itertools.product(*split))
            products = filter(lambda inter: best[0][0] >= fn(inter)[0], products)
            if deriv1 is not None:
                products = filter(lambda inter: all(interval([0.0]) in inter2 for inter2 in deriv1(inter)), products)
            intervals = intervals[1:] + products
            if verbose:
                print iteration
                print len(intervals)
                print best
                print best_x
    optimizer(intervals, 500000)
    return best_x

