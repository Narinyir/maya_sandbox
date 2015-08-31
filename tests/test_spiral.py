import math
import contextlib


class ParticleDisplay(object):

    def __init__(self, size):

        self.particle = cmds.particle()
        cmds.addAttr(self.particle[1], internalSet=True, ln="colorAccum",
                     at="bool", dv=False)
        cmds.addAttr(self.particle[1], internalSet=True, ln="useLighting",
                     at="bool", dv=False)
        cmds.addAttr(self.particle[1], internalSet=True, ln="pointSize",
                     at="long", min=1, max=60, dv=2)
        cmds.addAttr(self.particle[1], internalSet=True, ln="normalDir",
                     at="long", min=1, max=3, dv=2)
        cmds.setAttr(self.particle[1] + '.pointSize', size)

        self.to_curve = cmds.createNode('pointCloudToCurve')
        cmds.connectAttr(self.particle[1] + '.worldPosition',
                         self.to_curve + '.inArray')
        self.curve = cmds.createNode('nurbsCurve')
        cmds.connectAttr(self.to_curve + '.outCurve', self.curve + '.create')

    def add_points(self, *pnts):
        cmds.currentTime(cmds.currentTime(q=True) + 1)
        cmds.emit(object=self.particle[1], position=pnts)

    def __enter__(self):
        cmds.currentTime(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cmds.saveInitialState(self.particle[0])
        cmds.currentTime(1)
        return True


def make_spiral(radius=12, num_points=100):
    step = float(radius) / num_points

    for i in xrange(100):
        x = cos(i) * i * step
        y = sin(i) * i * step
        yield (x, y, 0)


def spiral_through_grid(point=(0, 0), distance=6):
    di = 0
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dv = dirs[0]
    for i in xrange(1, distance*2):
        for j in xrange(2):
            for k in xrange(i):
                point = (point[0] + dv[0], point[1] + dv[1])
                yield point
            di += 1
            dv = dirs[di % 4]


if __name__ == '__main__':
    with ParticleDisplay(size=4) as display:
        for pnt in spiral_through_grid():
            display.add_points([pnt[0], pnt[1], 0])
