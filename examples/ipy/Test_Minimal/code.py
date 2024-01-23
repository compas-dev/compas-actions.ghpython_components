"""
Do something silly.

This component does nothing useful, it's only a minimal example.

    Args:
        x: X value
        y: Y value
        z: Z value
    Returns:
        a: The sum of all three values.
"""

ghenv.Component.Message = 'COMPONENT v{{version}}'

a = x + y + z
