"""
Represents frame (plane) defined by one or few polygons.
"""
from svgwrite import shapes, path, mm, masking


class Pline(object):

    """ Absctract PolyLine class """

    def _draw(self):
        raise NotImplemented("Draw method is not yet implemented")


class Rect(Pline):

    """ Rectangle representation """

    def __init__(self, x, y, width, height):
        """
        x, y - coordinates of left top corner
        """
        self.corner = (x, y)
        self.size = (width, height)

    def _draw(self):
        return shapes.Rect(self.corner, self.size)

    def _mask(self):
        return False


class RectFrame(Pline):

    """ Rectangle frame representation """

    def __init__(self, x, y, width, height, wall_width):
        self.corner = (x * mm, y * mm)
        self.size = (width * mm, height * mm)
        self.inner_corner = ((x + wall_width) * mm, (y + wall_width) * mm)
        self.inner_size = ((width - 2 * wall_width) * mm, (height - 2 * wall_width) * mm)

    def _draw(self):
        rect = shapes.Rect(self.corner, self.size, **{"mask": "url(#rect-clip)", "stroke": "black", "stroke-width": "2", "fill": "#fff"})
        return rect

    def _mask(self):
        outer_rect = shapes.Rect(self.corner, self.size, fill="#FFF")
        inner_rect = shapes.Rect(self.inner_corner, self.inner_size, **{"fill": "#000", "stroke": "red", "stroke-width": "2"})
        mask = masking.Mask(id="rect-clip")
        mask.add(outer_rect)
        mask.add(inner_rect)
        return mask


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

    def add_rect_frame(self, x=0, y=0, width=1, height=1, wall_width=1):
        rect_frame = RectFrame(x, y, width, height, wall_width)
        self._plines.append(rect_frame)
        return rect_frame

    def _draw(self):
        return self._plines
