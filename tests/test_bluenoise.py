import sandbox
import bluenoise
reload(bluenoise)

def display_grid(grid):
    pass


def display_points(points):
    cmds.particle(position=points)


def test_bounded_poisson2D(bounds, min_dist, num_candidates):
    grid = bluenoise.bounded_poisson2D(bounds, min_dist, num_candidates)
    points = [[p.x, p.y, 0] for p in grid.points()]
    display_points(points)


def test_generate_bounded_poisson2D(bounds, min_dist, num_candidates):
    particle, particle_shape = cmds.particle()
    to_curve = cmds.createNode('pointCloudToCurve')
    cmds.connectAttr(particle_shape + '.worldPosition', to_curve + '.inArray')
    curve = cmds.createNode('nurbsCurve')
    cmds.connectAttr(to_curve + '.outCurve', curve + '.create')
    cmds.refresh()
    points = bluenoise.generate_bounded_poisson2D(bounds, min_dist, num_candidates)
    for i, p in enumerate(points):
        cmds.currentTime(i)
        cmds.emit(object=particle, position=(p.x, p.y, 0))


def test_poisson2D(num_points, min_dist, num_candidates):
    grid = bluenoise.poisson2D(num_points, min_dist, num_candidates)
    points = [[p.x, p.y, 0] for p in grid.points()]
    display_points(points)


def test_generate_poisson2D(num_points, min_dist, num_candidates):
    particle, particle_shape = cmds.particle()
    to_curve = cmds.createNode('pointCloudToCurve')
    cmds.connectAttr(particle_shape + '.worldPosition', to_curve + '.inArray')
    curve = cmds.createNode('nurbsCurve')
    cmds.connectAttr(to_curve + '.outCurve', curve + '.create')
    cmds.refresh()
    points = bluenoise.generate_poisson2D(num_points, min_dist, num_candidates)
    for i, p in enumerate(points):
        cmds.currentTime(i)
        cmds.emit(object=particle, position=(p.x, p.y, 0))


if __name__ == '__main__':
    test_generate_bounded_poisson2D(
        bounds=bluenoise.Bounds2([-12, -12], [12, 12]),
        min_dist=0.1,
        num_candidates=30,
        )

    # test_generate_poisson2D(
    #     num_points=10000,
    #     min_dist=0.5,
    #     num_candidates=32)
