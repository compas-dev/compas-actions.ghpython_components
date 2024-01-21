"""
Do something silly.

This component does nothing useful, it's only a kitchen sink example showing most available options.

    Args:
        x: X value
        y: Y value
        z: Z value
    Returns:
        result: The sum of all three values.
"""
# from ghpythonlib.componentbase import executingcomponent as component

import System
import Rhino
import Grasshopper

import rhinoscriptsyntax as rs


class MyComponent(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, x: float, y: float, z: float):
        self.Message = 'COMPONENT v{{version}}'
        result = x + y + z
        return result
