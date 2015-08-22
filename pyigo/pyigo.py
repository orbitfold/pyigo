import numpy as np
from interval import interval, imath
from math import fabs
import itertools

def bisect_simple(intervals):
    """Bisect a box by cutting along the longest edge.

    Arguments:
    ----------
    intervals --- a list of intervals representing the box

    Return:
    -------
    a list of lists of intervals representing the box after bisection
    """
    longest = max(range(len(intervals)), 
                  key=lambda i: fabs(intervals[i][0][1] - intervals[i][0][0]))
    longest_interval = intervals[longest]
    intervals1 = [interval(inter) for inter in intervals]
    intervals2 = [interval(inter) for inter in intervals]
    intervals1[longest] = interval([longest_interval[0][0], longest_interval.midpoint[0][0]])
    intervals2[longest] = interval([longest_interval.midpoint[0][0], longest_interval[0][1]])
    return [intervals1, intervals2]
    

def solve(fn, intervals, tolerance, deriv1=None, deriv2=None, verbose=True):
    best = [None]
    best_x = [None]
    intervals = [[interval(inter) for inter in intervals]]
    def optimizer(intervals):
        iteration = 0
        while not all([inter[0][1] - inter[0][0] < tolerance for inter in intervals[0]]):
            iteration += 1
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
                print "iteration:", iteration
                print "intervals to analyze:", len(intervals)
                print "best value:", best
                print "best solution:", best_x
                print
    optimizer(intervals)
    return best_x

