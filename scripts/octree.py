from maya.api import OpenMaya
from random import uniform
from collections import defaultdict
from functools import partial


class Bounds(object):

    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def expand(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def center(self):
        return (self.minimum + self.maximum) * 0.5

    def width(self):
        return self.maximum[0] - self.minimum[0]

    def height(self):
        return self.maximum[1] - self.minimum[1]

    def depth(self):
        return self.maximum[2] - self.minimum[2]

    @property
    def xmin(self):
        return self.minimum[0]

    @property
    def xmax(self):
        return self.maximum[0]

    @property
    def ymin(self):
        return self.minimum[1]

    @property
    def ymax(self):
        return self.maximum[1]

    @property
    def zmin(self):
        return self.minimum[2]

    @property
    def zmax(self):
        return self.maximum[2]

    def contains(self, pnt):
        return all(self.minimum[i] <= pnt[i] <= self.maximum[i]
                   for i in xrange(3))

    @classmethod
    def from_points(cls, pnts):
        x, y, z = zip(*pnts)
        minimum = [min(x), min(y), min(z)]
        maximum = [max(x), max(y), max(z)]
        return cls(minimum, maximum)


class OctreeNode(object):

    def __init__(self, index, bounds):
        self.index = index
        self.subnodes = []


minimum, maximum = OpenMaya.MVector(0, 0, 0), OpenMaya.MVector(10, 10, 10)
b1 = Bounds(minimum, maximum)

start = time.clock()
for i in xrange(1000000):
    b1.center()
print 'Cached bounds took: {} seconds'.format(time.clock() - start)

start = time.clock()
for i in xrange(100000):
    Bounds(minimum, maximum)
print 'Init Bounds1: {} seconds'.format(time.clock() - start)
