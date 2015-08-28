from random import randint
from operator import itemgetter
import time

grid = dict()

for i in xrange(10000):
    grid[(randint(0, 999999), randint(0, 999999))] = None


def sort_method(n):

    for i in xrange(n):
        xsort = sorted(grid.iterkeys(), key=itemgetter(0))
        ysort = sorted(grid.iterkeys(), key=itemgetter(1))
        xmin, xmax = xsort[0][0], xsort[-1][0]
        ymin, ymax = ysort[0][1], ysort[-1][1]

    print xmin, ymin
    print xmax, ymax


def minmax_method(n):

    for i in xrange(n):
        xmin = min(grid.iterkeys(), key=itemgetter(0))[0]
        xmax = max(grid.iterkeys(), key=itemgetter(0))[0]
        ymin = min(grid.iterkeys(), key=itemgetter(1))[1]
        ymax = max(grid.iterkeys(), key=itemgetter(1))[1]

    print xmin, ymin
    print xmax, ymax


def griderator_method(n):

    for i in xrange(n):
        griderator = grid.iterkeys()
        xmax, ymax = griderator.next()
        xmin, ymin = xmax, ymax
        for x, y in griderator:
            if x > xmax:
                xmax = x
            if x < xmin:
                xmin = x
            if y > ymax:
                ymax = y
            if y < ymin:
                ymin = y

    print xmin, ymin
    print xmax, ymax


def run_benchmarks(n):
    print 'Time averages after {} iterations'.format(n)

    start = time.clock()
    sort_method(n)
    print 'sort method: {}'.format((time.clock() - start) / n)

    start = time.clock()
    minmax_method(n)
    print 'minmax method: {}'.format((time.clock() - start) / n)

    start = time.clock()
    griderator_method(n)
    print 'griderator method: {}'.format((time.clock() - start) / n)


run_benchmarks(1)
