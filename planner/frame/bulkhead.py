from planner.frame.polygon import Polygon
from svgwrite import shapes, mm


class Bulkhead(Polygon):

    """
    Inner walls representation.
    Only horizontal and vertical bulkheads supported for now.
    """

    def __init__(self, left_top_point, right_bottom_point, **attribs):
        """
        left_top_point - coordinates of left-top Bulkhead corner
        right_bottom_point - coordinates of right-bottom Bulkhead corner
        """
        self.x = left_top_point[0]
        self.y = left_top_point[1]
        self.width = right_bottom_point[0] - left_top_point[0]
        self.height = right_bottom_point[1] - left_top_point[1]
        self.attribs = attribs

    def _draw(self):
        rect_params = {"stroke": "#000", "stroke-width": "2", "fill": "#fff"}
        rect_params.update(self.attribs)
        return shapes.Rect((self.x * mm, self.y * mm), (self.width * mm, self.height * mm), **rect_params)