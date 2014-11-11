"""
Represents frame (plane) defined by one or few polygons.
"""
from svgwrite import shapes


class Pline(object):

    """ Absctract PolyLine class """

    def _draw(self):
        raise NotImplemented("Draw method is not yet implemented")


class Rect(object):

    """ Rectangle representation """

    def __init__(self, x, y, width, height):
        """
        x, y - coordinates of left top corner
        """
        self.corner = (x, y)
        self.size = (width, height)

    def _draw(self):
        return shapes.Rect(self.corner, self.size)


class Frame(object):

    """
    Frame representation class. 
    """

    def __init__(self):
        self._plines = []

    def add_rect(self, x=0, y=0, width=1, height=1):
        """ Add rectangle to the frame and return it """
        rect = Rect(x, y, width, height)
        self._plines.append(rect)
        return rect

    def _draw(self):
        return self._plines
