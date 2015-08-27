import maya.cmds as cmds
import os
from functools import partial

__modname__ = 'maya_sandbox'
__modpath__ = cmds.moduleInfo(moduleName=__modname__, path=True)
__modversion__ = cmds.moduleInfo(moduleName=__modname__, version=True)

get_path = partial(os.path.join, __modpath__, '..', '..')
