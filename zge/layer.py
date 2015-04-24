"""
Rendering Layer Implementation
"""


import pygame


#=============================================================================
class Layer( object ):
    """
    Models a rendering layer in the scene.
    """

    #=========================================================================
    def __init__( self, surface = None, pos = None ):
        """
        Initializes a layer object.
        """
        if surface is None:
            rect = pygame.display.get_surface().get_rect()
            self.surface = pygame.Surface(
                ( rect.w, rect.h ),
                flags = pygame.SRCALPHA,
                depth = 32
            )
            self.surface.fill( ( 0, 0, 0, 0 ) )
        else:
            self.surface = surface
        self.pos = pos if pos is not None else ( 0, 0 )


    #=========================================================================
    def blit( self, surface ):
        """
        Blits this layer onto the given desination surface.
        """
        surface.blit( self.surface, self.pos )


#=============================================================================
class TextLayer( Layer ):
    """
    Specialized layer dedicated to displaying text.
    """

    #=========================================================================
    def __init__( self, *args, **kwargs ):
        """
        Initializes a TextLayer object.
        """
        super( TextLayer, self ).__init__( *args, **kwargs )
        self.font       = pygame.font.SysFont( 'Consolas', 16 )
        self.color      = ( 210, 210, 210 )
        self.background = None
        self.antialias  = True
        self._string    = None


    #=========================================================================
    def set_text( self, text ):
        """
        Sets the text displayed in the layer.
        """
        if self._string != text:
            self._string = text
            args = [ self._string, self.antialias, self.color ]
            if self.background is not None:
                args.append( self.background )
            rendered = self.font.render( *args )
            rect = rendered.get_rect()
            rect.x = self.pos[ 0 ]
            rect.y = self.pos[ 1 ]
            rwidth = rect.w
            rect.w = self.surface.get_rect().w
            self.surface.fill( ( 0, 0, 0, 0 ), rect )
            rect.w = rwidth
            self.surface.blit( self.font.render( *args ), rect )


#=============================================================================
class BlockTextLayer( TextLayer ):
    """
    A text layer that is expected to render one or more lines of text.
    """

    #=========================================================================
    def __init__( self, *args, **kwargs ):
        """
        Initializes a BlockTextLayer object.
        """
        super( BlockTextLayer, self ).__init__( *args, **kwargs )
        metrics = self.font.metrics( 'M@#' )
        self.line_spacing = self.font.get_linesize()
        self.cell_spacing = max( m[ 4 ] for m in metrics )
        self.glyph_width  = max( ( m[ 1 ] - m[ 0 ] ) for m in metrics )
        self.glyph_height = self.font.get_height()
        rect       = self.surface.get_rect()
        self.cols  = rect.w / self.cell_spacing
        self.rows  = rect.h / self.line_spacing
        self.lines = [ ( ' ' * self.cols ) ] * self.rows
        self._draw_lines()


    #=========================================================================
    def set_string( self, y, x, string ):
        """
        Sets a string starting at a given position in the text grid.
        Strings that would extend past the last column are clipped.
        y is the row with 0 being the top-most
        x is the column with 0 being left-most
        """

        # sanity check usage
        if y >= self.rows:
            raise ValueError(
                'Row value {} exceeds display {}'.format( y, self.rows )
            )
        if x >= self.cols:
            raise ValueError(
                'Column value {} exceeds display {}'.format( x, self.cols )
            )

        # clip string
        overflow = ( x + len( string ) ) - self.cols
        if overflow > 0:
            string = string[ : ( -1 * overflow ) ]

        # length of incoming string
        length = len( string )

        # see if this would actually change the display or not
        target = self.lines[ y ][ x : length ]
        if target != string:

            # position of this text when rendered
            ypos = y * self.line_spacing
            xpos = x * self.cell_spacing

            # render the new text
            args = [ string, self.antialias, self.color ]
            if self.background is not None:
                args.append( self.background )
            text = self.font.render( *args )

            # blit to display surface
            rect = text.get_rect()
            rect.x = xpos
            rect.y = ypos
            self.surface.fill( ( 0, 0, 0, 0 ), rect )
            self.surface.blit( text, ( xpos, ypos ) )


    #=========================================================================
    def set_text( self, text ):
        """
        Convenience method to display arbitrary strings on the layer.
        TODO: Add soft-wrapping support, and add a wrap control property.
        """
        text  = text.replace( '\r', '' )
        text  = text.replace( '\t', '    ' )
        lines = text.split( '\n' )
        row   = 0
        for line in lines:
            if row >= self.rows:
                break
            self.set_string( row, 0, line )
            row += 1


    #=========================================================================
    def _draw_lines( self ):
        """
        Draws all the lines of text onto the surface.
        """
        self.surface.fill( ( 0, 0, 0, 0 ) )
        y = 0
        for line in self.lines:
            args = [ line, self.antialias, self.color ]
            if self.background is not None:
                args.append( self.background )
            text = self.font.render( *args )
            self.surface.blit( text, ( 0, y ) )
            y += self.line_spacing

