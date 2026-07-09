"""
Do something silly in python3.

This component does nothing useful, it's only a kitchen sink (but in python3) example showing most available options.

    Args:
        x: X value
        y: Y value
        z: Z value
    Returns:
        result: The sum of all three values.
"""
from ghpythonlib.componentbase import executingcomponent as component

import System
import platform
import Rhino
import Grasshopper
import rhinoscriptsyntax as rs

import gh_timber
import importlib

importlib.reload(gh_timber)


class MyComponent(component):
    def RunScript(self, x: float, y: float, z: float):
        ghenv.Component.Message = 'COMPONENT v{{version}}'
        t = gh_timber.Timber(length=x, width=y, height=z)
        result = t.volume()
        return result
