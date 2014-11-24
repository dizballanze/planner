"""
Represents frame (plane) defined by one or few polygons.
"""
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
        style = "stroke: {color}; width: {width}".format(color=color, width=width * mm)
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

    def _is_point_on_line(self, line_start, line_end, point):
        """
        Check that point is lay on the line
        """
        crossproduct = (point[1] - line_start[1]) * (line_end[0] - line_start[0]) - (point[0] - line_start[0]) * (line_end[1] - line_start[1])
        if abs(crossproduct) > sys.float_info.epsilon:
            return False
        dotproduct = (point[0] - line_start[0]) * (line_end[0] - line_start[0]) + (point[1] - line_start[1]) * (line_end[1] - line_start[1])
        if dotproduct < 0:
            return False
        squaredlength = pow(line_end[0] - line_start[0], 2) + pow(line_end[1] - line_start[1], 2)
        if dotproduct > squaredlength:
            return False
        return True


class Rect(Polygon):

    """ Rectangle representation """

    def __init__(self, x=0, y=0, width=1, height=1, **attribs):
        """
        x, y - coordinates of left top corner
        """
        self.corner = (x * mm, y * mm)
        self.size = (width * mm, height * mm)
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


class RectFrame(Polygon):

    """ Rectangle frame representation """

    DEFAULT_PARAMS = {"stroke": "#000", "stroke-width": "2"}

    def __init__(self, x=0, y=0, width=1, height=1, wall_width=1, **attribs):
        self.corner = (x * mm, y * mm)
        self.size = (width * mm, height * mm)
        self.inner_corner = ((x + wall_width) * mm, (y + wall_width) * mm)
        self.inner_size = ((width - 2 * wall_width) * mm, (height - 2 * wall_width) * mm)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.wall_width = wall_width
        self.attribs = attribs or dict()
        self.apertures = []

    def _draw(self):
        rect_params = self.DEFAULT_PARAMS.copy()
        rect_params.update(self.attribs)
        res = []
        # Hatching and filling
        if hasattr(self, "hatch") and self.hatch:
            rect_params['style'] = "fill: url(#{})".format(self._hatching_id)
            res.append(self.hatch)
        if hasattr(self, "filling"):
            rect_params['fill'] = self.filling
        else:
            if 'fill' not in rect_params:
                rect_params['fill'] = "#fff"
        # Create outer and inner rects
        rect = shapes.Rect(self.corner, self.size, **rect_params)
        inner_rect = shapes.Rect(
            self.inner_corner, self.inner_size, **{"stroke": "#000", "stroke-width": "2", "fill": "#fff"})
        res.append(rect)
        res.append(inner_rect)
        # Apertures
        apertures = self._draw_apertures()
        if apertures:
            res = res + apertures
        return res

    def _draw_apertures(self):
        """
        Draw apertures
        """
        elements = []
        for aperture in self.apertures:
            attribs = {"stroke": "#000", "stroke-width": "2", "fill": "#fff"}
            attribs.update(aperture['attribs'])
            elements.append(
                shapes.Rect((aperture['x'] * mm, aperture['y'] * mm), (aperture['width'] * mm, aperture['height'] * mm), **attribs))
        return elements

    def _get_aperture_lines_coordinates(self):
        outer_lines = []
        # left
        outer_lines.append(((self.x, self.y + self.wall_width), (self.x, self.y + self.height - self.wall_width)))
        # top
        outer_lines.append(((self.x + self.wall_width, self.y), (self.x + self.width - self.wall_width, self.y)))
        # right
        outer_lines.append((
            (self.x + self.width - self.wall_width, self.y + self.wall_width),
            (self.x + self.width - self.wall_width, self.y + self.height - self.wall_width)))
        # bottom
        outer_lines.append((
            (self.x + self.wall_width, self.y + self.height - self.wall_width),
            (self.x + self.width - self.wall_width, self.y + self.height - self.wall_width)))
        return outer_lines

    def _get_border_name_by_point(self, lines, point):
        """
        Get border name (left, top, right, bottom) on which point located
        """
        if self._is_point_on_line(lines[0][0], lines[0][1], point):
            return 'left'
        if self._is_point_on_line(lines[1][0], lines[1][1], point):
            return 'top'
        if self._is_point_on_line(lines[2][0], lines[2][1], point):
            return 'right'
        if self._is_point_on_line(lines[3][0], lines[3][1], point):
            return 'bottom'
        return False

    def _is_point_on_lines(self, lines, point):
        return any([self._is_point_on_line(p[0], p[1], point) for p in lines])

    def add_aperture(self, x, y, width, **attribs):
        """
        Add aperture (door, window, etc) to the wall.
        x, y - coordinates of left-top corner, should be located on wall border
        """
        outer_lines = self._get_aperture_lines_coordinates()
        coords = (x, y)
        # Validate corner coordinates (should be correct left-top corner of door and lay on wall border)
        if not self._is_point_on_lines(outer_lines, coords):
            raise ValueError("Coordinates {}, {} of aparture left corner not located on the wall border".format(x, y))
        # Validate aperture width
        border = self._get_border_name_by_point(outer_lines, coords)
        if border in ['left', 'right']:
            aperture_end_coords = (x, y + width)
        if border in ['top', 'bottom']:
            aperture_end_coords = (x + width, y)
        if not self._is_point_on_lines(outer_lines, aperture_end_coords):
            raise ValueError("Specified width {} exceed wall sizes".format(width))
        if border in ['left', 'right']:
            self.apertures.append(dict(x=x, y=y, width=self.wall_width, height=width, attribs=attribs))
        elif border in ['top', 'bottom']:
            self.apertures.append(dict(x=x, y=y, width=width, height=self.wall_width, attribs=attribs))
