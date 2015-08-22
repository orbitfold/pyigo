from pyigo.pyigo import solve
from interval.imath import *
from interval import interval

offsets = [2.25, 3.00, -0.20, -2.00, -3.55, -1.59, -1.67, 0.77, 2.97, 2.07]

def rastrigin(args):
    return 10.0 * len(args) +\
        sum([(x - off) ** 2 - 10.0 * cos(2.0 * pi * (x - off)) 
             for x, off in zip(args, offsets)])

def rastrigin_deriv1(args):
    return [2.0 * (x - off) + 10.0 * 2.0 * pi * sin(2.0 * pi * (x - off))
            for x, off in zip(args, offsets)]

if __name__ == '__main__':
    solve(rastrigin, [[-5.12, 5.12]] * 5, 0.0001, deriv1=rastrigin_deriv1)
