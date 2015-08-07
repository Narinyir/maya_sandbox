from maya.api import OpenMaya
from math import sqrt
import random


def spheral_vector(vectype=OpenMaya.MFloatVector):
    '''Generate a random unit vector (Marsaglia 1972)

    :param vectype: Return type of vector
    '''

    d = 1
    while d >= 1:
        x0, x1 = random.uniform(-1, 1), random.uniform(-1, 1)
        d = x0**2 + x1**2

    x = 2 * x0 * sqrt(1 - x0**2 - x1**2)
    y = 2 * x1 * sqrt(1 - x0**2 - x1**2)
    z = 1 - 2 * d
    return vectype(x, y, z)


def hemispheral_vector(axis, vectype=OpenMaya.MFloatVector):
    '''Generate a random unit vector in the hemisphere defined by axis

    :param axis: OpenMaya.MVector representing axis of the hemisphere
    :param vectype: Return type of vector
    '''

    d = 1
    while d >= 1:
        x0, x1 = random.uniform(-1, 1), random.uniform(-1, 1)
        d = x0**2 + x1**2

    x = 2 * x0 * sqrt(1 - x0**2 - x1**2)
    y = 2 * x1 * sqrt(1 - x0**2 - x1**2)
    z = 1 - 2 * d
    result = vectype(x, y, z)
    if result * axis < 0:
        result = -result
    return result


def rotate_vectors(vectors, orientation, vectype=OpenMaya.MVector):

    q = OpenMaya.MVector.kYaxisVector.rotateTo(orientation)
    for v in vectors:
        yield vectype(v.rotateBy(q))


def time_em(n):

    import time
    import sys
    from contextlib import contextmanager


    @contextmanager
    def stopwatch(label, width=20):
        '''
        A context manager that prints out the execution time of the nested code.
        '''

        plat = sys.platform.rstrip('0123456789')
        time_fn = time.clock if plat == 'win' else time.time

        start = time_fn()
        try:
            yield
        finally:
            print '{:<{w}}: {}'.format(label, time_fn() - start, w=width)

    print '### {} Random Vectors ###'.format(n)

    with stopwatch('hemispheral_vector'):
        for i in xrange(n):
            hemispheral_vector(OpenMaya.MFloatVector(0, 1, 0))

    with stopwatch('spheral_vector'):
        for i in xrange(n):
            spheral_vector()
