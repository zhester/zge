#!/cygdrive/c/Python27/python.exe

"""
ZGE Windows Demo Program

The only reason this is for Windows is because I needed to hard-code the path
to my Windows Python binary.  It should work fine if invoked explicitly by any
Python interpreter.  Sorry for the hassle.
"""


# core packages
import os
import sys

# append path for running this script whithout installing the package
zge_path = os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) )
sys.path.append( zge_path )

# local package
import zge


__version__ = '0.0.0'


#=============================================================================
def start_demo():
    """
    Initializes and runs the demo "game."
    """

    # create a game engine object
    eng = zge.Engine( ( 640, 480 ) )

    ### ZIH - testing (abstracting all of this)
    import pygame
    surf  = pygame.Surface( ( 320, 240 ), flags = pygame.SRCALPHA )
    block = zge.layer.BlockTextLayer( surf, ( 40, 40 ) )
    eng._layers.append( block )
    block.set_text( '1. line 1\n2. line 2\nC. line C???' )

    # run the game loop until it exits (with its exit status)
    status = eng.run()

    # return to the shell
    return status


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv List of arguments passed to the script
    @return     Shell exit code (0 = success)
    """

    # imports when using this as a script
    import argparse

    # create and configure an argument parser
    parser = argparse.ArgumentParser(
        description = 'A Shell Script',
        add_help    = False
    )
    parser.add_argument(
        '-h',
        '--help',
        default = False,
        help    = 'Display this help message and exit.',
        action  = 'help'
    )
    parser.add_argument(
        '-v',
        '--version',
        default = False,
        help    = 'Display script version and exit.',
        action  = 'version',
        version = __version__
    )

    # parse the arguments
    args = parser.parse_args( argv[ 1 : ] )

    # start the demo "game"
    return start_demo()


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

