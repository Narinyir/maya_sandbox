from maya.api import OpenMaya
import occlusion
import sandbox

scene = sandbox.get_path('scenes', 'test_occlusion.ma')


def apply_ao(shape, num_rays, max_dist, falloff, random, smooth_iterations):

    sel = OpenMaya.MGlobal.getSelectionListByName(shape)
    dagpath = sel.getDagPath(0)
    start = time.clock()
    weight_per_vert = occlusion.calculate(
        dagpath,
        num_rays=num_rays,
        max_dist=max_dist,
        falloff=falloff,
        random=random,
        smooth_iterations=smooth_iterations)
    calc_time = time.clock() - start
    start = time.clock()
    color_per_vert = []
    for amount in weight_per_vert:
        amount = 1 - amount
        color_per_vert.append(OpenMaya.MColor([amount, amount, amount, 1]))

    mesh_fn = OpenMaya.MFnMesh(dagpath)
    mesh_fn.setVertexColors(color_per_vert, range(mesh_fn.numVertices))
    apply_time = time.clock() - start
    cmds.refresh()
    times = [
        'Calc Runtime: {} seconds'.format(calc_time),
        'Apply Runtime: {} seconds'.format(apply_time),
    ]
    return times


def run_benchmarks(scene, shape, ray_set, max_dist,
                   falloff, random, smooth_iterations):

    cmds.file(scene, open=True, force=True)
    sel = OpenMaya.MGlobal.getSelectionListByName(shape)
    dagpath = sel.getDagPath(0)
    mesh_fn = OpenMaya.MFnMesh(dagpath)
    for num_rays in ray_set:
        header = [
            'Calculating and applying AO',
            '    {} verts'.format(mesh_fn.numVertices),
            '    {} rays'.format(num_rays),
            '    {} maximum dist'.format(max_dist),
            '    {} smooth iterations'.format(smooth_iterations),
        ]
        if random:
            header[1] = '    {} random rays'.format(num_rays)
        print '\n'.join(header)

        start = time.clock()
        times = apply_ao(
            shape=shape,
            num_rays=num_rays,
            max_dist=max_dist,
            falloff=falloff,
            random=random,
            smooth_iterations=smooth_iterations)
        run_time = time.clock() - start
        times.append('Task Runtime: {} seconds'.format(run_time))
        print '\n'.join(times)


run_benchmarks(
    scene=scene,
    shape='testShape',
    ray_set=[48],
    max_dist=1,
    falloff=1,
    random=False,
    smooth_iterations=5
)
