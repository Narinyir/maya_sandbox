from maya.api import OpenMaya
import math
import random


PI = 3.14159265358
HPI = 1.57079632679
YAXIS = OpenMaya.MVector.kYaxisVector


def nonuniform_spherical_vector(radius=24):
    '''Horrible distribution'''

    angle = random.random() * 3.14 * 2
    dist = radius * sqrt(random.random())
    x = dist * cos(angle)
    y = dist * sin(angle)
    z = sqrt(radius * radius - dist * dist)
    if random.random() < 0.25 or random.random() > 0.25:
        z *= -1

    return OpenMaya.MVector(x, y, z)


def next_two_random():
    x0, x1 = random.uniform(-1, 1), random.uniform(-1, 1)
    d = x0**2 + x1**2
    if d > 1:
        return next_two_random()
    return x0, x1, d


def spheral_vector2():
    '''Generate a random unit vector using (Muller 1959, Marsaglia 1972)

    :returns: OpenMaya.MVector
    '''

    x = random.gauss(0, 1)
    y = random.gauss(0, 1)
    z = random.gauss(0, 1)
    s = 1 / sqrt(x**2 + y**2 + z**2)
    return OpenMaya.MVector(x, y, z) * s

def marsaglia_spherical_vector(radius=1):
    x0, x1, d = next_two_random()
    x = 2 * x0 * sqrt(1 - x0**2 - x1**2)
    y = 2 * x1 * sqrt(1 - x0**2 - x1**2)
    z = 1 - 2 * d
    return OpenMaya.MVector(x, y, z) * radius


def marsaglia_hemispheral_vector():
    x0, x1, d = next_two_random()
    x = 2 * x0 * sqrt(1 - x0**2 - x1**2)
    y = 2 * x1 * sqrt(1 - x0**2 - x1**2)
    z = 1 - 2 * d
    result = OpenMaya.MVector(x, y, z)
    if YAXIS * result < 0:
        result = -result
    return result


def marsaglia_hemispheral_vectors(n, orient, radius):
    q = YAXIS.rotateTo(orient)
    for i in xrange(n):
        v = marsaglia_hemispheral_vector()
        yield v.rotateBy(q) * radius


def marsaglia_hemispheral_points(n, center, orient, radius):

    q = YAXIS.rotateTo(orient)
    for i in xrange(n):
        v = marsaglia_hemispheral_vector()
        yield v.rotateBy(q) * radius + center


def next_four_random():
    x0, x1, x2, x3 = [random.uniform(-1, 1) for i in xrange(4)]
    d = x0**2 + x1**2 + x2**2 + x3**2
    if d > 1:
        return next_four_random()
    return x0, x1, x2, x3, d


def cook_spherical_vector(radius=10):
    x0, x1, x2, x3, d = next_four_random()
    d = 1/d
    x = (2 * (x1 * x3 + x0 * x2)) * d
    y = (2 * (x2 * x3 + x0 * x1)) * d
    z = (x0**2 + x3**2 - x1**2 - x2**2) * d
    return OpenMaya.MVector(x, y, z) * radius


def spheral_vectors(n, center, orient, radius):
    for i in xrange(n):
        yield spheral_vector(center, orient, radius)

def spheral_vector(center, orient, radius):
    rv = OpenMaya.MVector(*[random.gauss(-1, 1) for i in xrange(3)]).normal()
    q = OpenMaya.MQuaternion(random.uniform(-1, 1) * PI, rv)
    return orient.rotateBy(q) * radius + center

def hemispheral_vectors(n, center, orient, radius):
    for i in xrange(n):
        yield hemispheral_vector(center, orient, radius)

def hemispheral_vector(center, orient, radius):
    rv = OpenMaya.MVector(*[random.uniform(-1, 1) for i in xrange(3)]).normal()
    q = OpenMaya.MQuaternion(random.uniform(-1, 1) * HPI, rv)
    return orient.rotateBy(q) * radius + center


import time

def time_em(n):
    print '### {} hemispheral points ###'.format(n)

    center = OpenMaya.MVector(0, 10, 20)
    orient = OpenMaya.MVector(0.1, 0.5, 0.3).normal()
    radius = 1

    start = time.clock()
    hsphvs = hemispheral_vectors(
        n=n,
        center=center,
        orient=orient,
        radius=radius)
    list(hsphvs)
    print 'hemispheral_vectors: {}'.format(time.clock() - start)

    start = time.clock()
    hsphvs = marsaglia_hemispheral_vectors(
        n=n,
        center=center,
        orient=orient,
        radius=radius)
    list(hsphvs)
    print 'marsaglia_hemispheral_vectors: {}'.format(time.clock() - start)

# time_em(20000)


vectors = hemispheral_vectors(
    n=20000,
    center=OpenMaya.MVector(0, 0, -50),
    orient=YAXIS,
    radius=50)

for v in vectors:
    cmds.spaceLocator(position=v)


vectors = marsaglia_hemispheral_points(
    n=20000,
    center=OpenMaya.MVector(0, 0, 50),
    orient=YAXIS,
    radius=50)

for v in vectors:
    cmds.spaceLocator(position=v)
