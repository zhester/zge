"""
Zoe Game Engine Core Implementation
===================================

Requirements
------------

[pygame](http://www.pygame.org/)
"""

# core packages

# third-party packages
import pygame

# local package
import layer


__version__ = '0.0.0'


#=============================================================================
class Engine( object ):
    """
    Simple game engine object.
    """

    #=========================================================================
    def __init__( self, size ):
        """
        Initializes an Engine object.
        """

        # pygame initialization
        pygame.init()

        # initialize the root display surface
        self.window = pygame.display.set_mode( size, 0, 32 )

        # set the title bar text and iconification text
        pygame.display.set_caption( 'Demonstration', 'Demo' )

        # set the application icon
        icon = pygame.image.load( '../assets/z32.png' )
        pygame.display.set_icon( icon )

        # create a list of normal display layers
        self._layers = []

        # create a transparent "top" layer for overlayed information
        self._top = layer.TextLayer()

        # initialize last tick value
        self._last_tick = pygame.time.get_ticks()
        self._last_wait = 0

        # set an FPS cap
        self._fps       = 0.0
        self._fps_limit = 120.0
        self._tick_step = int( round( 1000.0 / self._fps_limit ) )


    #=========================================================================
    def run( self ):
        """
        Run the game loop (does not return until the application quits).
        """

        # update tick value before entering the loop
        self._last_tick = pygame.time.get_ticks()

        # execute infinite application loop
        done = False
        while done == False:

            # process event queue
            for event in pygame.event.get():

                # check for quit event
                if event.type == pygame.QUIT:
                    done = True

            # exit application loop if done
            if done == True:
                break

            # update the game display
            self.update()

            # ZIH - simulate hard work
            #pygame.time.delay( 3 )

            # compute duration of last event/render loop
            end_tick        = pygame.time.get_ticks()
            delta           = end_tick - self._last_tick
            self._last_tick = end_tick

            # update FPS value
            if delta > 0:
                self._fps = 1000.0 / float( delta )
            else:
                self._fps = self._fps_limit

            # compute remaining time available inside this iteration
            if delta < self._tick_step:
                self._last_wait = self._tick_step - delta
            else:
                self._last_wait = 0

            # let the OS do other stuff on this core
            pygame.time.wait( self._last_wait )

        # shut down pygame
        pygame.quit()

        # return exit status
        return 0


    #=========================================================================
    def update( self ):
        """
        Updates the display.
        """

        # update overlayed information
        self._top.set_text(
            ' [ fps:{:4.0f} sch:{:3} tck:{:08} ]'.format(
                self._fps,
                self._last_wait,
                self._last_tick
            )
        )

        # draw the display on the back buffer
        self._draw_layers()

        # update the display (swap video buffers)
        pygame.display.update()


    #=========================================================================
    def _draw_layers( self ):
        """
        Blits all the display layers onto the back buffer.
        """

        # fill the background
        self.window.fill( ( 32, 32, 32 ) )

        # blit all user layers
        for layer in self._layers:
            layer.blit( self.window )

        # blit the top layer
        self._top.blit( self.window )

