from planner.frame import Figure
from svgwrite import shapes


class Line(Figure):

    DEFAULT_ATTRIBS = {"stroke-width": 0.5, "stroke": "#000"}

    def __init__(self, start_point, end_point, **attribs):
        self.start_point = start_point
        self.end_point = end_point
        self.attribs = self.DEFAULT_ATTRIBS.copy()
        self.attribs.update(attribs)

    def _draw(self):
        return shapes.Line(self.start_point, self.end_point, **self.attribs)
