"""
Do something silly in cpy.

This component does nothing useful, it's only a kitchen sink (but in cpy) example showing most available options.

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


class MyComponent(component):
    def RunScript(self, x: float, y: float, z: float):
        ghenv.Component.Message = f"Cpy Version: {platform.python_version()}"
        result = x + y + z
        return result
