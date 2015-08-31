# from maya.api import OpenMaya
from collections import namedtuple
from random import uniform
from math import pi, floor, cos, sin
from Queue import Queue

vector2 = namedtuple('vector2', 'x y')
vector3 = namedtuple('vector3', 'x y z')


class Bounds2(object):
    '''2D Bounding Box object stored as two 2D vectors (minimum corner,
    maximum corner).

    usage::

        bounds = Bounds2(minimum=(-10, -10), maximum=(10, 10))
        assert bounds.contains(vector2(9, 1)) == True

        # OR

        from random import uniform
        pnts = [(uniform(-10, 10), uniform(-10, 10)) for i in xrange(1000)]
        bounds = Bounds2.from_points(pnts)
    '''

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

    def contains(self, pnt):
        return all(self.minimum[i] <= pnt[i] <= self.maximum[i]
                   for i in xrange(2))

    @classmethod
    def from_points(cls, pnts):
        x, y = zip(*pnts)
        minimum = [min(x), min(y)]
        maximum = [max(x), max(y)]
        return cls(minimum, maximum)


class Grid2D(dict):

    def __init__(self, cell_size):
        self.cell_size = cell_size

    def get_neighbors(self, x, y):
        neighbors = []
        candidates = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                      (x - 1, y), (x + 1, y),
                      (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        for candidate in candidates:
            if candidate in self:
                neighbors.append(self[candidate])
        return neighbors

    def bounds(self):
        cells = grid.iterkeys()
        xmax, ymax = cells.next()
        xmin, ymin = xmax, ymax
        for x, y in cells:
            if x > xmax:
                xmax = x
            if x < xmin:
                xmin = x
            if y > ymax:
                ymax = y
            if y < ymin:
                ymin = y
        return Bounds2((xmin, ymin), (xmax, ymax))

    # def get_nearest_neighbor(self, point):
    #     if not len(self):
    #         return None

    #     cell = self.get_cell(point)
    #     candidates = []
    #     while len(candidates) != 1:

    def get_cell(self, point):
        x = floor(point.x / self.cell_size)
        y = floor(point.y / self.cell_size)
        return x, y

    def points(self):
        return self.values()


def randisk(point, min_dist, vectype=vector2):
    radius = uniform(min_dist, 2 * min_dist)
    angle = 2 * pi * uniform(0, 1)
    x = point.x + (radius * cos(angle))
    y = point.y + (radius * sin(angle))
    return vectype(x, y)


def get_candidates(n, point, min_dist):
    for i in xrange(n):
        yield randisk(point, min_dist)


def generate_poisson2D(num_points, min_dist, num_candidates):

    start_point = vector2(0, 0)

    cell_size = min_dist * 0.5
    grid = Grid2D(cell_size)
    cell = grid.get_cell(start_point)
    grid[cell] = start_point

    process_queue = Queue()
    process_queue.put(start_point)

    while not process_queue.empty() and len(grid) < num_points:

        point = process_queue.get()
        yield point

        candidates = get_candidates(num_candidates, point, min_dist)
        for candidate in candidates:
            cell = grid.get_cell(candidate)
            if cell in grid or grid.get_neighbors(*cell):
                continue
            grid[cell] = candidate
            process_queue.put(candidate)


def poisson2D(num_points, min_dist, num_candidates):

    start_point = vector2(0, 0)

    cell_size = min_dist * 0.5
    grid = Grid2D(cell_size)
    cell = grid.get_cell(start_point)
    grid[cell] = start_point

    process_queue = Queue()
    process_queue.put(start_point)

    while not process_queue.empty() and len(grid) < num_points:

        point = process_queue.get()

        candidates = get_candidates(num_candidates, point, min_dist)
        for candidate in candidates:
            cell = grid.get_cell(candidate)
            if cell in grid or grid.get_neighbors(*cell):
                continue
            grid[cell] = candidate
            process_queue.put(candidate)

    return grid


def generate_bounded_poisson2D(bounds, min_dist, num_candidates):


    start_point = vector2(uniform(bounds.xmin, bounds.xmax),
                          uniform(bounds.ymin, bounds.ymax))

    cell_size = min_dist * 0.5
    grid = Grid2D(cell_size)
    cell = grid.get_cell(start_point)
    grid[cell] = start_point

    process_queue = Queue()
    process_queue.put(start_point)

    while not process_queue.empty():

        point = process_queue.get()
        yield point

        candidates = get_candidates(num_candidates, point, min_dist)
        for candidate in candidates:
            cell = grid.get_cell(candidate)
            if not bounds.contains(candidate):
                continue
            if cell in grid or grid.get_neighbors(*cell):
                continue
            grid[cell] = candidate
            process_queue.put(candidate)


def bounded_poisson2D(bounds, min_dist, num_candidates):


    start_point = vector2(uniform(bounds.xmin, bounds.xmax),
                          uniform(bounds.ymin, bounds.ymax))

    cell_size = min_dist * 0.5
    grid = Grid2D(cell_size)
    cell = grid.get_cell(start_point)
    grid[cell] = start_point

    process_queue = Queue()
    process_queue.put(start_point)

    while not process_queue.empty():

        point = process_queue.get()

        candidates = get_candidates(num_candidates, point, min_dist)
        for candidate in candidates:
            cell = grid.get_cell(candidate)
            if not bounds.contains(candidate):
                continue
            if cell in grid or grid.get_neighbors(*cell):
                continue
            grid[cell] = candidate
            process_queue.put(candidate)

    return grid
