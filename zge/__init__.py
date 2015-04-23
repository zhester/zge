"""
Zoe Game Engine Module Declarations
"""

#=============================================================================
__version__ = '0.0.0'

#=============================================================================
__all__ = [ 'engine', 'layer' ]

#=============================================================================
from . import *

#=============================================================================
# Expose "core" objects with simplified references.
#
#   This allows the following usage pattern:
#       import zge
#       my_game = zge.Engine()
#       class MyGame( zge.Engine ): ...
#
#   Rather than the more verbose (but still valid) pattern:
#       import zge
#       my_game = zge.engine.Engine()
#       class MyGame( zge.engine.Engine ): ...

Engine = engine.Engine

