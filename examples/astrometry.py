from interval.imath import *
import random
from pyigo.pyigo import solve

def shift(points, shift_x, shift_y):
    points = [list(point) for point in points]
    for point in points:
        point[0] += shift_x
        point[1] += shift_y
    return points

def rotate(points, origin, angle):
    points = [list(point) for point in points]
    for point in points:
        x = point[0]
        y = point[1]
        x_new = (x - origin[0]) * cos(angle) - (y - origin[1]) * sin(angle) + origin[0]
        y_new = (x - origin[0]) * sin(angle) + (y - origin[1]) * cos(angle) + origin[1]
        point[0] = x_new
        point[1] = y_new
    return points

def scale(points, origin, amount):
    points = [list(point) for point in points]
    for point in points:
        x = point[0] - origin[0]
        y = point[1] - origin[1]
        x *= amount
        y *= amount
        point[0] = x + origin[0]
        point[1] = y + origin[1]
    return points

def transform(points, origin, shift_x, shift_y, rotation, scale):
    points = [list(point) for point in points]
    for point in points:
        x = point[0] - origin[0]
        y = point[1] - origin[1]
        x_new = x * cos(rotation) - y * sin(rotation)
        y_new = x * sin(rotation) + y * cos(rotation)
        x_new *= scale
        y_new *= scale
        point[0] = x_new + origin[0] + shift_x
        point[1] = y_new + origin[1] + shift_y
    return points

def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def construct_function(points1, points2, origin):
    def function(x):
        transformed = transform(points2, origin, x[0], x[1], x[2], x[3])
        #transformed = shift(points2, x[0], x[1])
        #transformed = rotate(transformed, origin, x[2])
        #transformed = scale(transformed, origin, x[3])
        sum_distance = 0.0
        for p1 in transformed:
            closest = min(points1, key=lambda p2: distance(p1, p2))
            sum_distance += distance(p1, closest)
        return sum_distance
    return function
        
if __name__ == '__main__':
    initial = [[random.random(), random.random()] for _ in range(50)]
    cropped = [point for point in initial if 
               (point[0] > 0.4 and point[0] < 0.6) and 
               (point[1] > 0.4 and point[1] < 0.6)]
    cropped = transform(cropped, [0.5, 0.5], -0.1, 0.1, 2.0 * pi * 0.3, 2.0)
    #cropped = rotate(cropped, [0.5, 0.5], 2.0 * pi * 0.3)
    #cropped = scale(cropped, [0.5, 0.5], 2.0)
    #cropped = shift(cropped, -0.1, 0.1)
    fn = construct_function(initial, cropped, [0.5, 0.5])
    print fn([0.1, -0.1, -2.0 * pi * 0.3, 1.0 / 2.0])
    #solve(fn, [[-0.5, 0.5], [-0.5, 0.5], [-pi, pi], [0.001, 2.0]], 0.0001)
