from planner.frame.figure import Figure
from planner.frame.aperture import Aperture
from planner.frame.bulkhead import Bulkhead
from svgwrite import shapes


class RectFrame(Figure):

    """ Rectangle frame representation """

    DEFAULT_PARAMS = {"stroke": "#000", "stroke-width": "2"}

    def __init__(self, x=0, y=0, width=1, height=1, wall_width=1, **attribs):
        self.corner = (x, y)
        self.size = (width, height)
        self.inner_corner = (x + wall_width, y + wall_width)
        self.inner_size = (width - 2 * wall_width, height - 2 * wall_width)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.wall_width = wall_width
        self.attribs = attribs or dict()
        self.apertures = []
        self.bulkheads = []
        self.stroke_width = attribs.get('stroke-width') or self.DEFAULT_PARAMS.get('stroke-width')

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
        inner_params = self.DEFAULT_PARAMS.copy()
        inner_params.update(self.attribs)
        inner_params['fill'] = "#fff"
        inner_rect = shapes.Rect(
            self.inner_corner, self.inner_size, **inner_params)
        res.append(rect)
        res.append(inner_rect)
        # Apertures
        if self.apertures:
            for aperture in self.apertures:
                res.append(aperture._draw())
        # Bulkheads
        borders = []
        backgrounds = []
        if self.bulkheads:
            for bulkhead in self.bulkheads:
                border, *background = bulkhead._draw()
                borders.append(border)
                backgrounds.extend(background)
        res.extend(borders)
        res.extend(backgrounds)
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

    def _is_point_on_lines(self, lines, point):
        return any([self._is_point_on_line(p[0], p[1], point) for p in lines])

    def add_aperture(self, x, y, width, **attribs):
        """
        Add aperture (door, window, etc) to the wall.
        x, y - coordinates of left-top corner, should be located on wall border
        """
        outer_lines = self._get_aperture_lines_coordinates()
        coords = (x, y)
        # Propagate stroke-width
        if 'stroke-width' not in attribs:
            attribs['stroke-width'] = self.stroke_width
        aperture = Aperture.match_wall_and_create(coords, width, outer_lines, self.wall_width, **attribs)
        if not aperture:
            raise ValueError("Coordinates {}, {} of aparture left corner not located on the wall border".format(x, y))
        self.apertures.append(aperture)
        return aperture

    def add_bulkhead(self, x, y, width, **attribs):
        """
        Add bulkhead to current frame,
        x, y - should be coordinates of left-top corner and lay on left or top inner wall border
        """
        top_left_corner = (self.x + self.wall_width, self.y + self.wall_width)
        bottom_left_corner = (self.x + self.wall_width, self.y + self.height - 2 * self.wall_width)
        top_right_corner = (self.x + self.width - 2 * self.wall_width, self.y + self.wall_width)
        # horizontal
        if self._is_point_on_line(top_left_corner, bottom_left_corner, (x, y)):
            end_point = (x + self.width - 2 * self.wall_width, y + width)
        # vertical
        elif self._is_point_on_line(top_left_corner, top_right_corner, (x, y)):
            end_point = (x + width, y + self.height - 2 * self.wall_width)
        # error
        else:
            raise ValueError('Wrong coordinates, left-top corner should lay on left or top inner wall border')
        # Propagate stroke-width
        if 'stroke-width' not in attribs:
            attribs['stroke-width'] = self.stroke_width
        bulkhead = Bulkhead((x, y), end_point, **attribs)
        self.bulkheads.append(bulkhead)
        return bulkhead
