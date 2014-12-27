from svgwrite import shapes, mm, pattern
from shortuuid import uuid
import math
import sys


class Polygon(object):

    """ Absctract Polygon class """

    @property
    def uuid(self):
        if not hasattr(self, "_uuid"):
            self._uuid = uuid()
        return self._uuid

    def _draw(self):
        raise NotImplementedError("Draw method is not yet implemented")

    def _mask(self):
        return False

    @property
    def _hatching_id(self):
        return "hatching-{}".format(self.uuid)

    def add_hatching(self, angle=45, distance=3, width=1, color="#000"):
        """
        Add hatching to the walls.
        angle - angle of hatches in deg
        distance - distance between hatches
        width - stroke-width
        **Replaces all previously added hatchings or fillings.**
        """
        if hasattr(self, "filling"):
            del self.filling
        angle = math.radians(angle)
        style = "stroke: {color}; stroke-width: {width}".format(color=color, width=width * mm)
        pattern_width = distance / math.sin(angle)
        pattern_height = pattern_width * math.tan(angle)
        self.hatch = pattern.Pattern(
            (0 * mm, 0 * mm),
            (pattern_width * mm, pattern_height * mm), id=self._hatching_id, patternUnits="userSpaceOnUse")
        self.hatch.add(shapes.Rect((0 * mm, 0 * mm), (pattern_width * mm, pattern_height * mm), fill="#fff"))
        self.hatch.add(shapes.Line((0 * mm, 0 * mm), (pattern_width * mm, pattern_height * mm), style=style))
        self.hatch.add(
            shapes.Line((-1 * mm, (pattern_height - 1) * mm), (1 * mm, (pattern_height + 1) * mm), style=style))
        self.hatch.add(
            shapes.Line(((pattern_width - 1) * mm, -1 * mm), ((pattern_width + 1) * mm, 1 * mm), style=style))
        return self.hatch

    def add_filling(self, color):
        """
        Add solid filling of frame with specified color.
        **Replaces all previously added hatchings or fillings.**
        """
        if hasattr(self, 'hatch'):
            del self.hatch
        self.filling = color

    @classmethod
    def _is_point_on_line(cls, line_start, line_end, point):
        """
        Check that point is lay on the line
        """
        crossproduct = ((point[1] - line_start[1]) * (line_end[0] - line_start[0]) -
                        (point[0] - line_start[0]) * (line_end[1] - line_start[1]))
        if abs(crossproduct) > sys.float_info.epsilon:
            return False
        dotproduct = ((point[0] - line_start[0]) * (line_end[0] - line_start[0]) +
                      (point[1] - line_start[1]) * (line_end[1] - line_start[1]))
        if dotproduct < 0:
            return False
        squaredlength = pow(line_end[0] - line_start[0], 2) + pow(line_end[1] - line_start[1], 2)
        if dotproduct > squaredlength:
            return False
        return True
