# from maya.api import OpenMaya
from collections import namedtuple
from random import uniform
from math import pi

vector2 = namedtuple('vector2', 'x y')
vector3 = namedtuple('vector3', 'x y z')


class Grid2D(dict):

    def __init__(self, cell_width, cell_height):
        self.cell_width = cell_width
        self.cell_height = cell_height

    def get_neighbors(self, x, y):
        neighbors = []
        for x_offset in xrange(-1, 2):
            for y_offset in xrange(-1, 2):
                candidate = (x + x_offset, y + y_offset)
                if candidate in self:
                    neighbors.append(self[candidate])
        return neighbors

    def get_cell(self, point):
        x = floor(point.x / self.cell_width)
        y = floor(point.y / self.cell_height)
        return x, y


def randisk(point, min_dist, vectype=vector2):
    radius = uniform(min_dist, 2 * min_dist)
    angle = 2 * pi * uniform()
    x = point.x + radius * cos(angle)
    y = point.y + radius * cos(angle)
    return vectype(x, y)


