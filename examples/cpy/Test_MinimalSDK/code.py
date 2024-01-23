"""
Do something silly in Python3.

This component does nothing useful, it's only a minimal example in Python3.

    Args:
        x: X value
        y: Y value
        z: Z value
    Returns:
        a: The sum of all three values.
"""

from ghpythonlib.componentbase import executingcomponent as component

import platform

class MinimalSdkComponent(component):
    def RunScript(self, x, y, z):
        self.Message = f"Cpy Version: {platform.python_version()}"
        return (x + y + z)
