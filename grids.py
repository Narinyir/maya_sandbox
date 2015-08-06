from maya.api import OpenMaya
from random import uniform
from collections import defaultdict
from functools import partial


class OctreeNode(object):

    def __init__(self, center, half_width):
        self.center = center
        self.half_width = half_width
        self.subcells = []
        self.children = []


def random_points(n):
    r10 = partial(uniform, -1, 1)
    return (OpenMaya.MVector(r10(), r10(), r10()) for i in xrange(n))


def get_bounds2(points):

    x, y, z = zip(*points)

    min_corner = OpenMaya.MVector(min(x), min(y), min(z))
    max_corner = OpenMaya.MVector(max(x), max(y), max(z))

    center = (min_corner + max_corner) * 0.5
    halfwidth = center.length()

    return center, halfwidth

import time
start = time.clock()
points = random_points(100000)
bounds = get_bounds(points)
print bounds
print 'it took {} seconds'.format(time.clock() - start)

start = time.clock()
points = random_points(100000)
bounds = get_bounds2(points
)print bounds
print 'it took {} seconds'.format(time.clock() - start)
