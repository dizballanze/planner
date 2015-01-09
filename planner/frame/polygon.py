from planner.frame import Figure
from svgwrite import shapes


class Polygon(Figure):

    """
    Polygon figure.
    """

    DEFAULT_ATTRIBS = {"stroke": "#000", "stroke-width": "2", "fill": "#fff"}

    def __init__(self, points, **attribs):
        """
        `points` - iterable with tuples of coordinates (x, y)
        """
        self.points = points
        self.attribs = self.DEFAULT_ATTRIBS.copy()
        self.attribs.update(attribs)

    def _draw(self):
        res = []
        res = shapes.Polygon(self.points, **self.attribs)
        return res
