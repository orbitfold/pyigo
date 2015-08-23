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


def midpoint_test(fn_y, best_y):
    """Test if the best solution found so far is within the given interval.
    
    Arguments:
    ----------
    fn_y (interval) -- result of the function evaluation
    best_y (interval) -- best solution found so far

    Return:
    ------
    False if we should bisect the box, True if we should discard it
    """
    return best_y < fn_y


def monotonicity_test(d1_y):
    """Test if any of the coordinates is strictly monotonous within the given interval.
    
    Arguments:
    ----------
    d1_y (list of intervals) -- value of the function gradient

    Return:
    -------
    False if we should bisect the box, True if we should discard it
    """
    return not all([0.0 in inter for inter in d1_y])


def nonconvexity_test(d2_y):
    """Test if any of the coordinates is non-convex within the given interval

    Arguments:
    ----------
    d2_y (list of intervals) -- the diagonal of the Hessian matrix

    Return:
    -------
    False if we should bisect the box, True if we should discard it
    """
    return any([inter < 0.0 for inter in d2_y])


def solve(fn, intervals, precision, deriv1=None, deriv2=None, verbose=True):
    """Find the global optimum of a problem using interval arithmetic.

    Arguments:
    ----------
    fn (callable) -- a function to be optimized, must take a list of intervals and return an interval
    intervals (list of intervals) -- initial box
    precision (float) -- this is the interval size upon reaching which the algorithm will stop
    deriv1 (callable) -- first order derivative (gradient), must take a list of intervals and return a list of intervals
    deriv2 (callable) -- second order derivative (diagonal of the Hessian matrix), must take a list of intervals and return a list of intervals
    verbose (boolean) -- whether to output information to the screen when running

    Return:
    -------
    Global optimum within a given precision
    """
    best = [None]
    best_x = [None]
    intervals = [[interval(inter) for inter in intervals]]
    def optimizer(intervals):
        iteration = 0
        dropped = 0
        # Stop when the largest interval is smaller than the specified precision
        while not max([inter[0][1] - inter[0][0] for inter in intervals[0]]) < precision:
            iteration += 1
            # Evaluate the function at the midpoint of the given interval
            mid = [inter.midpoint for inter in intervals[0]]
            mid_y = fn(mid)
            if best[0] is None or mid_y < best[0]:
                best[0] = mid_y
                best_x[0] = mid
            if (midpoint_test(fn(intervals[0]), best[0]) or
                (deriv1 is not None and monotonicity_test(deriv1(intervals[0]))) or
                (deriv2 is not None and nonconvexity_test(deriv2(intervals[0])))):
                intervals = intervals[1:]
                dropped += 1
            else:
                intervals = intervals[1:] + bisect_simple(intervals[0])
            if verbose:
                print "intervals: analyzed=%s dropped=%s left=%s" % (iteration, dropped, len(intervals))
                print "best value:", best[0][0][0]
                print "best solution:", [x[0][0] for x in best_x[0]]
                print
    optimizer(intervals)
    return best_x

