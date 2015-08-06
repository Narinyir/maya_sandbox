import time
num_verts = 10000

start = time.clock()
weights, sampled = zip(*((0.0, False) for i in xrange(num_verts)))
print 'zipped in: {}'.format(time.clock() - start)

start = time.clock()
weights = []
sampled = []
for i in xrange(num_verts):
    weights.append(0.0)
    sampled.append(False)
print 'iterated in: {}'.format(time.clock() - start)
