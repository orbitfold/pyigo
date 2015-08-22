from interval import interval
from pyigo.pyigo import bisect_simple

def test_bisect_simple():
    box = [interval([0.0, 0.1]), interval([0.2, 0.6]), interval([0.1, 0.3])]
    bisected = bisect_simple(box)
    correct = [[interval([0.0, 0.1]), interval([0.2, 0.4]), interval([0.1, 0.3])],
               [interval([0.0, 0.1]), interval([0.4, 0.6]), interval([0.1, 0.3])]]
    assert all([inter1 == inter2 for inter1, inter2 in zip(bisected, correct)])
