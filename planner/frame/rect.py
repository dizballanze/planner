from planner.frame.figure import Figure
from svgwrite import shapes


class Rect(Figure):

    """ Rectangle representation """

    def __init__(self, x=0, y=0, width=1, height=1, **attribs):
        """
        x, y - coordinates of left top corner
        """
        self.corner = (x, y)
        self.size = (width, height)
        self.attribs = attribs

    def _draw(self):
        res = []
        rect_params = self.attribs.copy()
        if hasattr(self, "hatch") and self.hatch:
            rect_params['style'] = "fill: url(#{})".format(self._hatching_id)
            res.append(self.hatch)
        if hasattr(self, "filling"):
            rect_params['fill'] = self.filling
        else:
            if 'fill' not in self.attribs:
                rect_params['fill'] = "#fff"
        rect = shapes.Rect(self.corner, self.size, **rect_params)
        res.append(rect)
        return res
