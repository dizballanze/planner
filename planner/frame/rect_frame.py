from planner.frame.polygon import Polygon
from planner.frame.aperture import Aperture
from svgwrite import shapes, mm


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
        if self.apertures:
            for aperture in self.apertures:
                res.append(aperture._draw())
        return res

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
        aperture = Aperture.match_wall_and_create(coords, width, outer_lines, self.wall_width)
        if not aperture:
            raise ValueError("Coordinates {}, {} of aparture left corner not located on the wall border".format(x, y))
        self.apertures.append(aperture)
